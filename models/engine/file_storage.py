#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        result = {}
        if not cls:
            return FileStorage.__objects
        for key in self.__objects:
            if type(self.__objects[key]) == cls:
                result[key] = FileStorage.__objects[key]
        return result

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    index = key.split('.')[0]
                    self.all()[key] = classes[index](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """public method to delete obj from __objects in case of existence"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if self.__objects[key]:
                del self.__objects[key]

    def close(self):
        """ 
            calls the reload() method for deserialization from the JSON file to objects 
        """
        self.reload()
