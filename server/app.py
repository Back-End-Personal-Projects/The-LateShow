from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models.episode import Episode
from models.guest import Guest
from models.appearance import Appearance
from flask_restful import Resource, Api
from flask import jsonify
from db import db

# Create Flask app
app = Flask(__name__)
api = Api(app)

#Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)
migrate = Migrate(app, db)

class Index(Resource):
    def get(self):
        return "Welcome to the Late Show API!"
api.add_resource(Index, '/')

#Building the API

#Episode
class Episodi(Resource):
    # Get all episodes
    def get(self):
        episodes = []
        for episode in Episode.query.all():
            episode_dict = episode.to_dict()
            episodes.append(episode_dict)

        response = make_response(jsonify(episodes),200) 

        return response
    
    #Create new episode
    
    def post(self):
        data = request.get_json()

        if not all(key in data for key in ('date', 'number')):
            return jsonify({"error": "Missing required fields: date, number"}), 400

        new_episode = Episode(
            date=data['date'],
            number=data['number']
        )
        
        db.session.add(new_episode)
        db.session.commit()

        return make_response(jsonify(new_episode.to_dict()), 201)
    
api.add_resource(Episodi, '/episodes')

    #Get episode by ID
class EpisodebyID(Resource):
    def get(self,id):
        episode = Episode.query.filter(Episode.id == id).first()

        if not episode:
            return jsonify({"error": "Episode not found"}), 404
        
        Episode_dict = episode.to_dict()

        response = make_response(jsonify(Episode_dict),200)

        return response

        #Update episodes
    
    def put(self,id):
        episode = Episode.query.get(id)
        if not episode:
            return jsonify({"error": "Episode not found"}), 404

        data = request.get_json()
        episode.date = data.get('date', episode.date)
        episode.number = data.get('number', episode.number)
        db.session.commit()
        return make_response(jsonify(episode.to_dict()), 200)

    # Update episode (PATCH)
    
    def patch(self, id):
        episode = Episode.query.get_or_404(id)  

        data = request.get_json()  

        if 'date' in data:
            episode.date = data['date']
        if 'number' in data:
            episode.number = data['number']

        db.session.commit()  
        return make_response(jsonify(episode.to_dict()), 200) 

    # Delete an episode
    def delete(self,id):
        episode = Episode.query.get_or_404(id)  

        db.session.delete(episode)  
        db.session.commit()  

        return make_response(jsonify({"message": "Episode deleted successfully."}), 200)

api.add_resource(EpisodebyID, '/episodes/<int:id>')

#GUESTS
  
class Mgeni(Resource):
    # Get all guests
    def get(self):
        guests = []  
        for guest in Guest.query.all():
            guest_dict = guest.to_dict()
            guests.append(guest_dict)

        response = make_response(jsonify(guests) ,200) 
        return response
    
    #Create new guest
    
    def post(self):
        data = request.get_json()
        new_guest = Guest(
            name=data['name'],
            occupation=data['occupation']
        )
        
        db.session.add(new_guest)
        db.session.commit()
        response = new_guest.to_dict()
        response_body = make_response(jsonify(response), 201) 
        return response_body
    
api.add_resource(Mgeni, '/guests')

    #Get guest by ID
    
class GuestbyID(Resource):
    def get(user,id):
        guest = Guest.query.filter(Guest.id == id).first()
        
        if not guest:
            return jsonify({"error": "Guest not found"}), 404
        
        Guest_dict = guest.to_dict()

        response = make_response(Guest_dict,200)

        return response
    
    #Update guests
    
    def put(self,id):
        guest = Guest.query.get(id)
        if not guest:
            return jsonify({"error": "Guest not found"}), 404

        data = request.get_json()
        guest.name = data.get('name', guest.name)
        guest.occupation = data.get('occupation', guest.occupation)
        db.session.commit()
        return make_response(jsonify(guest.to_dict()), 200)

    # Update guest (PATCH)
    
    def patch(self, id):
        guest = Guest.query.get_or_404(id)  

        data = request.get_json()  

        if 'name' in data:
            guest.name = data['name']
        if 'occupation' in data:
            guest.occupation = data['occupation']

        db.session.commit()  
        return make_response(jsonify(guest.to_dict()), 200)

    # Delete a guest
    
    def delete(self,id):
        guest = Guest.query.get_or_404(id)  

        db.session.delete(guest)  
        db.session.commit()  

        return make_response(jsonify({"message": "Guest deleted successfully."}), 200)
    
api.add_resource(GuestbyID, '/guests/<int:id>')
  

class Appearanc (Resource):
    #APPEARANCE

        # Get all appearances
        
        def get(self):
            appearances = [] 
            for appearance in Appearance.query.all():
                appearance_dict = appearance.to_dict()
                appearances.append(appearance_dict)

            response = make_response(jsonify(appearances),200)

            return response

        #Create new appearance
        
        def post(self):
            data = request.get_json()
            try:
                #rating = data['rating']
                #validate_rating(rating)

                new_appearance = Appearance(
                    rating=data['rating'],
                    episode_id=data['episode_id'],
                    guest_id=data['guest_id'],
                )
            
                db.session.add(new_appearance)
                db.session.commit()

                return make_response(jsonify(new_appearance.to_dict()), 201)
            
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            
api.add_resource(Appearanc,'/appearances')           

class AppearancebyID(Resource):           
        #Get appearances by ID
        
        def get(self, id):
            appearance = Appearance.query.filter(Appearance.id == id).first()
            
            if not appearance:
                return jsonify({"error": "Appearance not found"}), 404
        
            appearance_dict = jsonify(appearance.to_dict())

            response = make_response(appearance_dict,200)

            return response

        


        #Update appearance
        
        def put(self, id):
            appearance = Appearance.query.get(id)
        
            data = request.get_json()
            #if 'rating' in data:
                #validate_rating(data['rating'])
            appearance.rating = data['rating']

            appearance.episode_id = data.get('episode_id', appearance.episode_id)
            appearance.guest_id = data.get('guest_id', appearance.guest_id)
        
            db.session.commit()
            return make_response(jsonify(appearance.to_dict()), 200)

    # Update appearance (PATCH)
    
        def patch(self, id):
            appearance = Appearance.query.get_or_404(id)  

            data = request.get_json()  

            if 'rating' in data:
                appearance.rating = data['rating']
            if 'episode_id' in data:
                appearance.episode_id = data['episode_id']
            if 'guest_id' in data:
                appearance.guest_id = data['guest_id']

            db.session.commit()  
            return make_response(jsonify(appearance.to_dict()), 200) 

        # Delete a appearance
        
        def delete(self, id):
            appearance = Appearance.query.get_or_404(id)  

            db.session.delete(appearance)  
            db.session.commit()  

            return make_response(jsonify({"message": "Appearance deleted successfully."}), 200)

api.add_resource(AppearancebyID,'/appearances/<int:id>')

if __name__ == '__main__':
     app.run(debug=True)