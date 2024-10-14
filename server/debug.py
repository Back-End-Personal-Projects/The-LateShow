from app import app
from db import db
from models.appearance import Appearances
from models.episode import Episodes
from models.guest import Guests



if __name__ == '__main__':
    
    with app.app_context():
        import ipdb; ipdb.set_trace()