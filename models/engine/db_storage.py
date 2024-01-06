#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ return all objects """
        all_obj_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    all_obj_dict[key] = obj
        return (all_obj_dict)

    def new(self, obj):
        """ add a new object to the current database """
        self.__session.add(obj)

    def save(self):
        """ save all changes of the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete object from the current database """
        if obj is not None:
            self.__session.delete(obj)

    def get(self, cls, id):
        """ gets an object """
        from models import storage
        result = self.all(cls)
        for item in result.values():
            if item.id == id:
                return item
        return None

    def count(self, cls=None):
        """ returns count of object """
        from models import storage
        total = 0

        if cls:
            all_data = storage.all(cls).values()
        else:
            all_data = storage.all().values()

        for _ in all_data:
            total += 1
        return total

    def reload(self):
        """ reloads the database"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session

    def close(self):
        """ call remove() method to close database """
        self.__session.remove()
