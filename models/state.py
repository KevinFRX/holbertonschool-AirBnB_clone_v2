#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.city import City
from os import getenv
import models
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    """new: ORM configuration"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'states'
        name = Column(String(128),
                      nullable=False)
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete")

    # FIX: for FileStorage with getter attribute
    if STORAGE_TYPE == 'fs':
        name = ''

        @property
        def cities(self):
            new_list = []
            for key, value in models.storage.all(City).items():
                if self.id == value.state_id:
                    new_list.append(value)
            return new_list
