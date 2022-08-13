#!/usr/bin/python3
"""ORM implementation: DBStorage definition"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base


class DBStorage():
    """class definition"""
    __engine = None

    __session = None

    def __init__(self):
        """__init__"""
        sql_user = getenv('HBNB_MYSQL_USER')
        sql_password = getenv('HBNB_MYSQL_PWD')
        sql_host = getenv('HBNB_MYSQL_HOST')
        sql_database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f"mysql+mysqldb://{sql_user}:{sql_password}@{sql_host}:3306/{sql_database}", pool_pre_ping=True)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Fetch objects from tables in function of the class"""
        res = {}
        objs = []
        if cls is None:
            str_classes = ['State', 'City', 'Place',
                           'Amenity', 'Review', 'User']
            for str in str_classes:
                qry = self.__session.query(eval(str))
                for objects in qry:
                    objs.append(objects)
        else:
            objs = self.__session.query(cls).all()
        for obj in objs:
            key = f"{type(obj).__name__}.{obj.id}"
            res[key] = obj
        return res

    def new(self, obj):
        """add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
