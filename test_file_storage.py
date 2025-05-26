#!/usr/bin/python3
"""
Unittest for FileStorage class
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

class TestFileStorage(unittest.TestCase):
    """Test FileStorage functionality"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip for DBStorage")
    def test_all_returns_dict(self):
        fs = FileStorage()
        self.assertIsInstance(fs.all(), dict)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip for DBStorage")
    def test_new_and_save(self):
        fs = FileStorage()
        bm = BaseModel()
        fs.new(bm)
        key = "BaseModel." + bm.id
        self.assertIn(key, fs.all())
        fs.save()
        with open("file.json", "r") as f:
            self.assertIn(bm.id, f.read())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip for DBStorage")
    def test_reload(self):
        fs = FileStorage()
        fs.reload()
        self.assertIsInstance(fs.all(), dict)

if __name__ == "__main__":
    unittest.main()

