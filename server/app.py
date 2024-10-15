from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.episode import Episode
from models.guest import Guest
from models.appearance import Appearance
from flask import jsonify
from db import db

# Create Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Late Show API!"

#Building the API
#Episode
# Get all episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = []
    for episode in Episode.query.all():
        episode_dict = episode.to_dict()
        episodes.append(episode_dict)

    response = jsonify(episodes),200

    return response

#Get episode by ID
@app.route('/episodes/<int:id>', methods=['GET'])
def episodes_by_id(id):
    episode = Episode.query.filter(Episode.id == id).first()

    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    Episode_dict = episode.to_dict()

    response = make_response(Episode_dict,200)

    return response

#Create new episode
@app.route('/episodes', methods=['POST'])
def create_episode():
    data = request.get_json()

    if not all(key in data for key in ('date', 'number')):
        return jsonify({"error": "Missing required fields: date, number"}), 400

    new_episode = Episode(
        date=data['date'],
        number=data['number']
    )
    
    db.session.add(new_episode)
    db.session.commit()

    return jsonify(new_episode.to_dict()), 201

#Update episodes
@app.route('/episodes/<int:id>', methods=['PUT'])
def update_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    data = request.get_json()
    episode.date = data.get('date', episode.date)
    episode.number = data.get('number', episode.number)
    db.session.commit()
    return jsonify(episode.to_dict()), 200

# Update episode (PATCH)
@app.route('/episodes/<int:id>', methods=['PATCH'])
def patch_episode(id):
    episode = Episode.query.get_or_404(id)  

    data = request.get_json()  

    if 'date' in data:
        episode.date = data['date']
    if 'number' in data:
        episode.number = data['number']

    db.session.commit()  
    return jsonify(episode.to_dict()), 200 

# Delete an episode
@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get_or_404(id)  

    db.session.delete(episode)  
    db.session.commit()  

    return jsonify({"message": "Episode deleted successfully."}), 200 

#GUESTS
# Get all guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = []
    for guest in Guest.query.all():
        guest_dict = guest.to_dict()
        guests.append(guest_dict)

    response = jsonify(guests),200

    return response

#Get guest by ID
@app.route('/guests/<int:id>', methods=['GET'])
def guests_by_id(id):
    guest = Guest.query.filter(Guest.id == id).first()
    
    if not guest:
        return jsonify({"error": "Guest not found"}), 404
    
    Guest_dict = guest.to_dict()

    response = make_response(Guest_dict,200)

    return response

#Create new guest
@app.route('/guests', methods=['POST'])
def create_guest():
    data = request.get_json()
    new_guest = Guest(
        name=data['name'],
        occupation=data['occupation']
    )
    
    db.session.add(new_guest)
    db.session.commit()

    return jsonify(new_guest.to_dict()), 201

#Update guests
@app.route('/guests/<int:id>', methods=['PUT'])
def update_guest(id):
    guest = Guest.query.get(id)
    if not guest:
        return jsonify({"error": "Guest not found"}), 404

    data = request.get_json()
    guest.name = data.get('name', guest.name)
    guest.occupation = data.get('occupation', guest.occupation)
    db.session.commit()
    return jsonify(guest.to_dict()), 200

# Update guest (PATCH)
@app.route('/guests/<int:id>', methods=['PATCH'])
def patch_guest(id):
    guest = Guest.query.get_or_404(id)  

    data = request.get_json()  

    if 'name' in data:
        guest.name = data['name']
    if 'occupation' in data:
        guest.occupation = data['occupation']

    db.session.commit()  
    return jsonify(guest.to_dict()), 200 

# Delete a guest
@app.route('/guests/<int:id>', methods=['DELETE'])
def delete_guest(id):
    guest = Guest.query.get_or_404(id)  

    db.session.delete(guest)  
    db.session.commit()  

    return jsonify({"message": "Guest deleted successfully."}), 200

#APPEARANCE
# Validation Function
def validate_rating(rating):
    if not (1 <= rating <= 5):
        raise ValueError(f"Rating must be between 1 and 5, but got {rating}.")

# Get all appearances
@app.route('/appearances', methods=['GET'])
def get_appearances():
    appearances = []
    for appearance in Appearance.query.all():
        appearance_dict = appearance.to_dict()
        appearances.append(appearance_dict)

    response = jsonify(appearances),200

    return response

#Get appearances by ID
@app.route('/appearances/<int:id>', methods=['GET'])
def appearances_by_id(id):
    appearance = Appearance.query.filter(Appearance.id == id).first()
    
    if not appearance:
        return jsonify({"error": "Appearance not found"}), 404
   
    appearance_dict = appearance.to_dict()

    response = make_response(appearance_dict,200)

    return response

#Create new appearance
@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        rating = data['rating']
        validate_rating(rating)

        new_appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id'],
        )
    
        db.session.add(new_appearance)
        db.session.commit()

        return jsonify(new_appearance.to_dict()), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


#Update appearance
@app.route('/appearances/<int:id>', methods=['PUT'])
def update_appearance(id):
    appearance = Appearance.query.get(id)
   
    data = request.get_json()
    if 'rating' in data:
        validate_rating(data['rating'])
        appearance.rating = data['rating']

    appearance.episode_id = data.get('episode_id', appearance.episode_id)
    appearance.guest_id = data.get('guest_id', appearance.guest_id)
   
    db.session.commit()
    return jsonify(appearance.to_dict()), 200

# Update appearance (PATCH)
@app.route('/appearances/<int:id>', methods=['PATCH'])
def patch_appearance(id):
    appearance = Appearance.query.get_or_404(id)  

    data = request.get_json()  

    if 'rating' in data:
        validate_rating(data['rating'])
        appearance.rating = data['rating']
    if 'episode_id' in data:
        appearance.episode_id = data['episode_id']
    if 'guest_id' in data:
        appearance.guest_id = data['guest_id']

    db.session.commit()  
    return jsonify(appearance.to_dict()), 200 

# Delete a appearance
@app.route('/appearances/<int:id>', methods=['DELETE'])
def delete_appearance(id):
    appearance = Appearance.query.get_or_404(id)  

    db.session.delete(appearance)  
    db.session.commit()  

    return jsonify({"message": "Appearance deleted successfully."}), 200  

if __name__ == '__main__':
    app.run(debug=True)