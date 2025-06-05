i#!/usr/bin/env python3
"""
Test BaseModel - PEP8 compliant
File: tests/test_models/test_base_model.py
"""

import unittest
import os
from datetime import datetime
from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def setUp(self):
        """Set up test environment"""
        pass

    def tearDown(self):
        """Clean up after tests"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            try:
                os.remove("file.json")
            except FileNotFoundError:
                pass

    def test_base_model_creation(self):
        """Test BaseModel instance creation"""
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)
        self.assertTrue(hasattr(model, 'id'))
        self.assertTrue(hasattr(model, 'created_at'))
        self.assertTrue(hasattr(model, 'updated_at'))

    def test_base_model_id_is_string(self):
        """Test that id is string"""
        model = BaseModel()
        self.assertIsInstance(model.id, str)

    def test_base_model_created_at_is_datetime(self):
        """Test that created_at is datetime"""
        model = BaseModel()
        self.assertIsInstance(model.created_at, datetime)

    def test_base_model_updated_at_is_datetime(self):
        """Test that updated_at is datetime"""
        model = BaseModel()
        self.assertIsInstance(model.updated_at, datetime)

    def test_base_model_unique_ids(self):
        """Test that each instance has unique id"""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_base_model_str_representation(self):
        """Test string representation"""
        model = BaseModel()
        string = str(model)
        self.assertIn("BaseModel", string)
        self.assertIn(model.id, string)

    def test_base_model_save_method(self):
        """Test save method updates updated_at"""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(old_updated_at, model.updated_at)

    def test_base_model_to_dict_method(self):
        """Test to_dict method"""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')

    def test_base_model_to_dict_contains_all_attributes(self):
        """Test to_dict contains all attributes"""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    def test_base_model_to_dict_datetime_format(self):
        """Test to_dict datetime format"""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)

    def test_base_model_from_dict_creation(self):
        """Test creation from dictionary"""
        model = BaseModel()
        model_dict = model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(model.id, new_model.id)

    def test_base_model_from_dict_datetime_conversion(self):
        """Test datetime conversion from dict"""
        model = BaseModel()
        model_dict = model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)

    def test_base_model_kwargs_creation(self):
        """Test creation with kwargs"""
        kwargs = {
            'id': 'test-id',
            'created_at': '2023-01-01T00:00:00.000000',
            'updated_at': '2023-01-01T00:00:00.000000'
        }
        model = BaseModel(**kwargs)
        self.assertEqual(model.id, 'test-id')

    def test_base_model_kwargs_ignores_class(self):
        """Test that __class__ is ignored in kwargs"""
        kwargs = {
            '__class__': 'SomeClass',
            'id': 'test-id'
        }
        model = BaseModel(**kwargs)
        self.assertEqual(model.__class__.__name__, 'BaseModel')

    def test_base_model_new_instance_in_storage(self):
        """Test new instance is in storage"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            model = BaseModel()
            key = "BaseModel.{}".format(model.id)
            self.assertIn(key, storage.all())

    def test_base_model_save_updates_storage(self):
        """Test save updates storage"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            model = BaseModel()
            key = "BaseModel.{}".format(model.id)
            old_updated_at = storage.all()[key].updated_at
            model.save()
            self.assertNotEqual(old_updated_at,
                                storage.all()[key].updated_at)


class TestStateModel(unittest.TestCase):
    """Test State model"""

    def setUp(self):
        """Set up test environment"""
        pass
