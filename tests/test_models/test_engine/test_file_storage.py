#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import sys
import pep8
import unittest
from unittest.mock import patch
from io import StringIO
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """ Tests to check the documentation and style of FileStorage class """
    @classmethod
    def setUpClass(cls):
        """ Set up for the doc tests """
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conform_file_storage(self):
        """Test PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_file_storage(self):
        """Test PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_docstring(self):
        """ Test FileStorage class docstring """
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_func_docstrings(self):
        """ Test for docstrings in FileStorage methods """
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        all_obj_dict = storage.all()
        self.assertEqual(type(all_obj_dict), dict)
        self.assertIs(all_obj_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """ test new """
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        all_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instant = value()
                instance_key = instant.__class__.__name__ + "." + instant.id
                storage.new(instant)
                all_dict[instance_key] = instant
                self.assertEqual(all_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """ Test save """
        storage = FileStorage()
        all_obj_dict = {}
        for key, value in classes.items():
            instant = value()
            instance_key = instant.__class__.__name__ + "." + instant.id
            all_obj_dict[instance_key] = instant
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = all_obj_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in all_obj_dict.items():
            all_obj_dict[key] = value.to_dict()

        string = json.dumps(all_obj_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """ Test filestorage count """
        self.assertEquals(len(models.storage.all().values()),
                          models.storage.count())

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """ Test files storage get """
        state_id = State(name="NY")
        state_id.save()
        models.storage.reload()
        self.assertEquals((models.storage.get("State", state_id.id)).id,
                          state_id.id)
