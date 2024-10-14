from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

class Appearance(db.Model):
    __tablename__ = 'appearances'

    serialize_rules =('-guest.appearances', '-episode.appearances',)

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    episode_id = Column(Integer, ForeignKey('episodes.id',ondelete='CASCADE'), nullable=False)
    guest_id = Column(Integer, ForeignKey('guests.id',ondelete='CASCADE'), nullable=False)

    # Relationships
    episode = relationship('Episode', back_populates='appearances')
    guest = relationship('Guest', back_populates='appearances')

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