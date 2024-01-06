#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """ check the pep8 style """
    @classmethod
    def setUpClass(cls):
        """ Set up """
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8(self):
        """ Test for PEP8."""
        pep_test = pep8.StyleGuide(quiet=True)
        response = pep_test.check_files(['models/engine/db_storage.py'])
        self.assertEqual(response.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_db_storage(self):
        """ Test test_db_storage.py conforms to PEP8."""
        pep_test = pep8.StyleGuide(quiet=True)
        response = pep_test.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(response.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_docstring(self):
        """ Test db_storage.py docstring """
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_docstring(self):
        """ Test DBStorage docstring """
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_db_functs_docstrings(self):
        """ Test docstrings in DBStorage methods"""
        for funct in self.dbs_f:
            self.assertIsNot(funct[1].__doc__, None,
                             "{:s} method needs a docstring".format(funct[0]))
            self.assertTrue(len(funct[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(funct[0]))


class TestFileStorage(unittest.TestCase):
    """ Test the FileStorage class """
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all(self):
        """ Test all returns dict """
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_parameter(self):
        """Test all when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new_func(self):
        """test new """

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorage(unittest.TestCase):
    """confirm storage db is working"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_get(self):
        """ Tests get functtion """
        new_state = State(name="NY")
        new_state.save()
        new_user = User(email="fun@fun.com", password="pwd")
        new_user.save()

        self.assertIs(new_state, models.storage.get("State", new_state.id))
        self.assertIs(None, models.storage.get("State", "abc"))
        self.assertIs(None, models.storage.get("meh", "abc"))
        self.assertIs(new_user, models.storage.get("User", new_user.id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_count(self):
        """ Tests count function """
        total = models.storage.count()
        self.assertEqual(models.storage.count("Blah"), 0)

        new_state = State(name="NY")
        new_state.save()
        new_user = User(email="fun@fun.com", password="pwd")
        new_user.save()

        self.assertEqual(models.storage.count("State"), total + 1)
        self.assertEqual(models.storage.count(), total + 2)
