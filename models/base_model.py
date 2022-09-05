#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from uuid import uuid4, UUID
from os import getenv

STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')

"""
    Creates instance of Base if storage type is a database
    If not database storage, uses class Base
"""
if STORAGE_TYPE == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
    A base class for all hbnb models
    ***reviewed***
    """
    if STORAGE_TYPE == 'db':
        """ adding ORM configuration"""
        id = Column(String(60),
                    primary_key=True,
                    nullable=False)

        created_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow())

        updated_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow())
    """---------------------------------------"""

    def __init__(self, *args, **kwargs):
        """
            instantiation of new BaseModel Class
        """
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()

    def __set_attributes(self, kwargs):
        """
            private: converts kwargs values to python class
            attributes
        """
        try:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
        except Exception:
            self.updated_at = datetime.now()
        try:
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
        except Exception:
            self.created_at = datetime.now()
        try:
            del kwargs['__class__']
        except Exception:
            pass
        if 'id' not in kwargs:
            self.id = str(uuid.uuid4())
        self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        try:
            del self.__dict__['_sa_instance_state']
        except Exception:
            pass
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """
        Updates updated_at with current time when instance is
        changed
        """
        from models import storage
        self.updated_at = datetime.now()
        """new: 1 row"""
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)

        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})

        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        """new: 2 rows: remove the key _sa_instance_state"""
        try:
            if dictionary['_sa_instance_state']:
                del dictionary['_sa_instance_state']
        except Exception:
            pass
        return dictionary

    def delete(self):
        """
          delete the current instance from the storage
          new:the whole function

          from models import storage
          storage.delete(self)
        """
        key = self.__class__ + self.id
        from models import storage
        del storage.__objects[key]
