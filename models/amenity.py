#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import backref
from models.place import place_amenity
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """Amenity class handles all application amenities"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            'Place', secondary=place_amenity)
    else:
        name = ''
