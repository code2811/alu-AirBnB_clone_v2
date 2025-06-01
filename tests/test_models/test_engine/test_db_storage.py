#!/usr/bin/python3
"""
Test cases for DBStorage engine
"""

import unittest
import os
import MySQLdb
from unittest import skipIf
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from models.user import User


@skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
        "Database storage tests only")
class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage class"""

    def setUp(self):
        """Set up test fixtures"""
        self.storage = DBStorage()
        
        
        try:
            self.db = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
                user=os.getenv('HBNB_MYSQL_USER', 'hbnb_test'),
                passwd=os.getenv('HBNB_MYSQL_PWD', 'hbnb_test_pwd'),
                db=os.getenv('HBNB_MYSQL_DB', 'hbnb_test_db')
            )
            self.cursor = self.db.cursor()
        except Exception:
            self.skipTest("MySQL database not available")

    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'db') and self.db:
            self.db.close()

    def test_db_storage_instantiation(self):
        """Test DBStorage instantiation"""
        self.assertIsInstance(self.storage, DBStorage)

    def test_db_storage_all(self):
        """Test all method returns dictionary"""
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)

    def test_db_storage_new_save(self):
        """Test new and save methods"""
        
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]
        
       
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()
        
        
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_count = self.cursor.fetchone()[0]
        self.assertEqual(final_count - initial_count, 1)
        
        
        self.cursor.execute(
            "SELECT name FROM states WHERE id = %s", (state.id,)
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "California")

    def test_db_storage_delete(self):
        """Test delete method"""
        
        state = State(name="ToDelete")
        state.save()
        
      
        self.cursor.execute(
            "SELECT COUNT(*) FROM states WHERE id = %s", (state.id,)
        )
        count_before = self.cursor.fetchone()[0]
        self.assertEqual(count_before, 1)
        
       
        self.storage.delete(state)
        self.storage.save()
        
       
        self.cursor.execute(
            "SELECT COUNT(*) FROM states WHERE id = %s", (state.id,)
        )
        count_after = self.cursor.fetchone()[0]
        self.assertEqual(count_after, 0)

    def test_db_storage_reload(self):
        """Test reload method"""
        
        state = State(name="TestReload")
        state.save()
        
        
         new_storage = DBStorage()
        new_storage.reload()
        
  
        all_objects = new_storage
