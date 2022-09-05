#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    """ The city class, contains state ID and name
         and now we modify it to suppor ORM and new
        requirements
    """
    if STORAGE_TYPE == "db":
        __tablename__ = 'cities'
        name = Column(String(128),
                      nullable=False)
        state_id = Column(String(60),
                          ForeignKey('states.id'),
                          nullable=False)
        places = relationship("Place",
                              backref='cities',
                              cascade="all, delete-orphan")
    if STORAGE_TYPE != 'db':
        state_id = ''
        name = ''
        places = []
