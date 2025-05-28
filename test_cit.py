#!/usr/bin/python3
"""Test cases for City model"""

import unittest
import os
import MySQLdb
from models.city import City
from models.state import State
from models import storage


class TestCity(unittest.TestCase):
    """Test City model"""
    
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

    def test_city_creation(self):
        """Test basic city creation"""
        city = City()
        self.assertIsInstance(city, City)
        self.assertTrue(hasattr(city, 'id'))
        self.assertTrue(hasattr(city, 'name'))
        self.assertTrue(hasattr(city, 'state_id'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Skip for non-database storage")
    def test_city_with_state_db(self):
        """Test city creation with state in database"""
        # Create a state first
        state = State()
        state.name = "California"
        state.save()
        
        # Create city with state_id
        city = City()
        city.name = "San Francisco"
        city.state_id = state.id
        city.save()
        
        # Verify in database
        self.cursor.execute(
            "SELECT name, state_id FROM cities WHERE id = %s", (city.id,)
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "San Francisco")
        self.assertEqual(result[1], state.id)

    # Add more tests following the same pattern...


if __name__ == '__main__':
    unittest.main()
