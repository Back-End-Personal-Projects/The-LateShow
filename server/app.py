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
app.json.compact = False

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

    Episode_dict = episode.to_dict()

    response = make_response(Episode_dict,200)

    return response

#Create new episode
@app.route('/episodes', methods=['POST'])
def create_episode():
    data = request.get_json()
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