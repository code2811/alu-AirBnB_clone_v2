#!/usr/bin/python3
"""
Test cases for State model
"""

import unittest
import os
import MySQLdb
from unittest import skipIf
from datetime import datetime
from models import storage
from models.state import State
from models.city import City


class TestState(unittest.TestCase):
    """Test cases for State model"""

    def setUp(self):
        """Set up test fixtures"""
        self.storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')
        
        # Set up MySQL connection for database tests
        if self.storage_type == 'db':
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

    def test_state_creation(self):
        """Test basic State creation"""
        state = State()
        self.assertIsInstance(state, State)
        self.assertTrue(hasattr(state, 'id'))
        self.assertTrue(hasattr(state, 'created_at'))
        self.assertTrue(hasattr(state, 'updated_at'))
        self.assertTrue(hasattr(state, 'name'))

    def test_state_with_name(self):
        """Test State creation with name"""
        state = State(name="California")
        self.assertEqual(state.name, "California")

    def test_state_str_representation(self):
        """Test State string representation"""
        state = State()
        state.name = "Texas"
        state_str = str(state)
        self.assertIn("State", state_str)
        self.assertIn(state.id, state_str)

    @skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
            "Database storage only")
    def test_state_save_to_database(self):
        """Test saving State to database"""
        # Get initial count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]
        
        # Create and save state
        state = State(name="Nevada")
        state.save()
        
        # Check final count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_count = self.cursor.fetchone()[0]
        
        self.assertEqual(final_count - initial_count, 1)
        
        # Verify state data in database
        self.cursor.execute(
            "SELECT name FROM states WHERE id = %s", (state.id,)
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Nevada")

    @skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 
            "File storage only")
    def test_state_save_to_file(self):
        """Test saving State to file storage"""
        initial_count = len([obj for obj in storage.all().values() 
                           if type(obj) is State])
        
        state = State(name="Oregon")
        state.save()
        
        final_count = len([obj for obj in storage.all().values() 
                         if type(obj) is State])
        
        self.assertEqual(final_count - initial_count, 1)

    @skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
            "Database storage only")
    def test_state_cities_relationship(self):
        """Test State-City relationship"""
        state = State(name="Florida")
        state.save()
        
        city = City(name="Miami", state_id=state.id)
        city.save()
        
        # Check relationship in database
        self.cursor.execute(
            "SELECT COUNT(*) FROM cities WHERE state_id = %s", 
            (state.id,)
        )
        city_count = self.cursor.fetchone()[0]
        self.assertEqual(city_count, 1)

    def test_state_to_dict(self):
        """Test State to_dict method"""
        state = State(name="Washington")
        state_dict = state.to_dict()
        
        self.assertIsInstance(state_dict, dict)
        self.assertEqual(state_dict['__class__'], 'State')
        self.assertEqual(state_dict['name'], 'Washington')
        self.assertIn('id', state_dict)
        self.assertIn('created_at', state_dict)
        self.assertIn('updated_at', state_dict)

    def test_state_kwargs_creation(self):
        """Test State creation with kwargs"""
        state_dict = {
            'name': 'Idaho',
            'id': '1234-5678-9012',
            'created_at': '2023-01-01T12:00:00.000000',
            'updated_at': '2023-01-01T12:00:00.000000'
        }
        state = State(**state_dict)
        self.assertEqual(state.name, 'Idaho')
        self.assertEqual(state.id, '1234-5678-9012')

    def test_state_update(self):
        """Test State update functionality"""
        state = State(name="Montana")
        old_updated_at = state.updated_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        state.name = "New Montana"
        state.save()
        
        self.assertNotEqual(old_updated_at, state.updated_at)
        self.assertEqual(state.name, "New Montana")


if __name__ == '__main__':
    unittest.main()
