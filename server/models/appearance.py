from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from db import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    serialize_rules =('-guest.appearances', '-episode.appearances',)

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, ForeignKey('episodes.id',ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, ForeignKey('guests.id',ondelete='CASCADE'), nullable=False)

    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    #Validations
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError(f"Rating must be between 1 and 5, but got {rating}.")
        return rating

    def to_dict(self):
        return{
            "id": self.id,
            "rating": self.rating,
            "episode_id": self.episode_id,
            "guest_id": self.guest_id,
            "episode": self.episode.to_dict() if self.episode else None,
            "guest": self.guest.to_dict() if self.guest else None}
    
    def __repr__(self):
        return (f"<Appearance(id={self.id}, "
                f"rating={self.rating}, "
                f"guest_id={self.guest_id}, "
                f"episode_id={self.episode_id})>")