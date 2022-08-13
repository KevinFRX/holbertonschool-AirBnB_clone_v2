#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
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
        cities = relationship('City',
                              backref='state',
                              cascade='delete')
    else:
        name = ''

        @property
        def cities(self):
            """returns the list of City instances with state_id
            equals to the current State.id
            """
            cityList = []
            for city in models.storage.all("City").values():
                if self.id == city.state_id:
                    cityList.append(city)
            return cityList
