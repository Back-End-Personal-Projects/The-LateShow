from faker import Faker
from random import randint, choice
from db import db
from models.episode import Episode
from models.guest import Guest
from models.appearance import Appearance
from app import app

fake = Faker()

def seed_data():
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()

        def create_fake_episodes(n):
            episodes = []
            for _ in range(n):
                episode = Episode(
                    date=fake.date(),
                    number=randint(1, 100)  
                )
                episodes.append(episode)
            return episodes

        def create_fake_guests(n):
            guests = []
            for _ in range(n):
                guest = Guest(
                    name=fake.name(),
                    occupation=fake.job(),
                )
                guests.append(guest)
            return guests

        def create_fake_appearances(episodes, guests, n):
            appearances = []
            for _ in range(n):
                # Select random episode and guest
                episode = choice(episodes)
                guest = choice(guests)
                appearance = Appearance(
                    rating=randint(1, 5),
                    episode_id=episode.id,  
                    guest_id=guest.id       
                )
                appearances.append(appearance)
            return appearances

        n_episodes = 10  
        n_guests = 15  
        n_appearances = 20  

        # Create fake episodes and guests
        episodes = create_fake_episodes(n_episodes)
        guests = create_fake_guests(n_guests)

        # Add episodes and guests to the session
        db.session.add_all(episodes)
        db.session.add_all(guests)
        db.session.commit() 

        # Create and add appearances
        appearances = create_fake_appearances(episodes, guests, n_appearances)
        db.session.add_all(appearances)  
        db.session.commit()  

        print("Seeding complete!")

if __name__ == "__main__":
    seed_data()  