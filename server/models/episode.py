from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from models.appearance import Appearance

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    serialize_rules = ('-appearance.episode',)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    #Relationship mapping episode to appearance
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    #Association proxy to access guests directly
    guests = association_proxy('appearances', 'guest')

    def to_dict(self):
        return{
            "id": self.id,
            "date": self.date,
            "number": self.number,
         }
    
def __repr__(self):
    return (f"<Episode (id={self.id},"
           f"date='{self.date}',"
           f"number={self.number}),"
           f"guests={self.guest})>")