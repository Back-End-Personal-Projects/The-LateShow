from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from models.appearance import Appearance



class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    serialize_rules = ('-appearances.guest',)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    occupation = Column(String, nullable=False)

    # Relationship mapping guest to appearances
    appearances = relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    # Association proxy to access episodes directly
    episodes = association_proxy('appearances', 'episode')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ocupation": self.occupation,
         }

    def __repr__(self):
        return f"<Guest(id={self.id}, name='{self.name}'), occupation='{self.occupation}')>"