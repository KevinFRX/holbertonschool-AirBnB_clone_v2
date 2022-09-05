#!/usr/bin/python3
"""
Place Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey,\
    MetaData, Table, ForeignKey
from sqlalchemy.orm import backref
import models
from models.review import Review

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == "db":

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey(
                              'places.id'), primary_key=True),
                          Column('amenity_id', String(60), ForeignKey
                                 ('amenities.id'), primary_key=True))


class Place(BaseModel, Base):
    """Place class handles all application places"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        amenities = relationship(
            'Amenity', secondary=place_amenity,
            back_populates='place_amenities', viewonly=False)

        reviews = relationship('Review', backref='place',
                               cascade='all, delete')
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
        review_ids = []

        @property
        def reviews(self):
            new_list = []
            instance_review = models.storage.all[Review]

            for key, value in instance_review:
                if self.id == value.place_id:
                    new_list.append(value)
            return new_list

        @property
        def amenities(self):
            """
                getter for amenitiess list, i.e. amenities attribute of self
            """
            if len(self.amenity_ids) > 0:
                return self.amenity_ids
            else:
                return None

        @amenities.setter
        def amenities(self, amenity_obj):
            """
                setter for amenity_ids
            """
            if amenity_obj and amenity_obj not in self.amenity_ids:
                self.amenity_ids.append(amenity_obj.id)
