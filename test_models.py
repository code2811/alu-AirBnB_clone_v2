#!/usr/bin/python3
"""Test cases for State model"""

import unittest
import os
import MySQLdb
from models.state import State
from models import storage
from datetime import datetime
import uuid


class TestState(unittest.TestCase):
    """Test State model"""
    
    def setUp(self):
        """Set up test environment"""
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.db = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            self.cursor = self.db.cursor()
        
    def tearDown(self):
        """Clean up after tests"""
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.cursor.close()
            self.db.close()
        else:
            try:
                os.remove("file.json")
            except FileNotFoundError:
                pass

    def test_state_creation(self):
        """Test basic state creation - works with both storage types"""
        state = State()
        self.assertIsInstance(state, State)
        self.assertTrue(hasattr(state, 'id'))
        self.assertTrue(hasattr(state, 'created_at'))
        self.assertTrue(hasattr(state, 'updated_at'))
        self.assertTrue(hasattr(state, 'name'))

    def test_state_attributes(self):
        """Test state attributes - works with both storage types"""
        state = State()
        state.name = "California"
        self.assertEqual(state.name, "California")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 
                     "Skip for database storage")
    def test_file_storage_save(self):
        """Test saving state to file storage"""
        state = State()
        state.name = "Texas"
        state.save()
        
        # Check if object is in storage
        key = f"State.{state.id}"
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Skip for non-database storage")
    def test_database_save(self):
        """Test saving state to database"""
        # Get initial count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]
        
        # Create and save state
        state = State()
        state.name = "Florida"
        state.save()
        
        # Check database count increased
        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchone()[0]
        self.assertEqual(new_count, initial_count + 1)
        
        # Verify the state exists in database
        self.cursor.execute("SELECT name FROM states WHERE id = %s", (state.id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Florida")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Skip for non-database storage")
    def test_database_delete(self):
        """Test deleting state from database"""
        # Create state
        state = State()
        state.name = "ToDelete"
        state.save()
        state_id = state.id
        
        # Get count before delete
        self.cursor.execute("SELECT COUNT(*) FROM states")
        before_count = self.cursor.fetchone()[0]
        
        # Delete state
        state.delete()
        storage.save()
        
        # Check database count decreased
        self.cursor.execute("SELECT COUNT(*) FROM states")
        after_count = self.cursor.fetchone()[0]
        self.assertEqual(after_count, before_count - 1)
        
        # Verify the state doesn't exist in database
        self.cursor.execute("SELECT COUNT(*) FROM states WHERE id = %s", (state_id,))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0)

    def test_to_dict(self):
        """Test to_dict method - works with both storage types"""
        state = State()
        state.name = "Nevada"
        state_dict = state.to_dict()
        
        self.assertIsInstance(state_dict, dict)
        self.assertIn('__class__', state_dict)
        self.assertEqual(state_dict['__class__'], 'State')
        self.assertIn('name', state_dict)
        self.assertEqual(state_dict['name'], 'Nevada')

    def test_str_representation(self):
        """Test string representation - works with both storage types"""
        state = State()
        state.name = "Arizona"
        string_rep = str(state)
        self.assertIn(state.__class__.__name__, string_rep)
        self.assertIn(state.id, string_rep)


if __name__ == '__main__':
    unittest.main()
