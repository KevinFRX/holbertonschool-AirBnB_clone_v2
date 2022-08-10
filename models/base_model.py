#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import os
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

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
        """Instatntiates a new model"""
        if not kwargs:
            """from models import storage"""
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            """storage.new(self)"""
        else:
            ()
            try:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')
                del kwargs['__class__']
                self.__dict__.update(kwargs)
            except KeyError:
                print("Inexistent key")
            except Exception:
                exit

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        try:
            del self.__dict__['_sa_instance_state']
        except:
            pass
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
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
        if dictionary['_sa_instance_state']:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """
          delete the current instance from the storage
          new:the whole function
        """
        from models import storage
        storage.delete(self)
