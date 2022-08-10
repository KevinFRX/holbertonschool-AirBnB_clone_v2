#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey,\
    MetaData, Table, ForeignKey
from sqlalchemy.orm import backref
from models import storage
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


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

        amenities = relationship('Amenity', secondary="place_amenity",
                                 viewonly=False)
        reviews = relationship('Review', backref='place', cascade='delete')
        amenity_ids = []
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
        """reviews getter"""
        lista = []
        reviews = storage.all("Review")
        for x in self.reviews.values():
            if x.place_id == self.id:
                lista.append(x)
        return (lista)

    @property
    def amenities(self):
        """amenities getter"""
        return amenity_ids

    @amenities.setter
    def amenities(self, obj):
        """amenities setter"""
        if type(obj) == "Amenity":
            amenity_ids.append(obj.id)

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey(
                              'places.id'), nullable=False),
                          Column('amenity_id', String(60), ForeignKey(
                              'amenities.id'), nullable=False)
                          )
