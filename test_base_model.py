#!/usr/bin/python3
"""
Unittest for BaseModel class
"""
import os
import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Test BaseModel functionality"""

    def test_instantiation(self):
        bm = BaseModel()
        self.assertIsInstance(bm, BaseModel)
        self.assertIsInstance(bm.id, str)
        self.assertIsInstance(bm.created_at, type(bm.updated_at))

    def test_save_and_updated_at(self):
        bm = BaseModel()
        old_updated = bm.updated_at
        bm.save()
        self.assertNotEqual(bm.updated_at, old_updated)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip for DBStorage")
    def test_to_dict(self):
        bm = BaseModel()
        d = bm.to_dict()
        self.assertIsInstance(d, dict)
        self.assertIn('id', d)
        self.assertIn('created_at', d)
        self.assertIn('updated_at', d)

if __name__ == "__main__":
    unittest.main()

