#!/usr/bin/python3
"""
Test cases for FileStorage engine
"""

import unittest
import os
import json
from unittest import skipIf
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User


@skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 
        "File storage tests only")
class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Set up test fixtures"""
        self.storage = FileStorage()
        self.test_file = "test_file.json"
        
        # Create a clean test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_file_storage_instantiation(self):
        """Test FileStorage instantiation"""
        self.assertIsInstance(self.storage, FileStorage)

    def test_file_storage_all(self):
        """Test all method returns dictionary"""
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)

    def test_file_storage_new(self):
        """Test new method adds object to storage"""
        state = State(name="California")
        initial_count = len(self.storage.all())
        
        self.storage.new(state)
        final_count = len(self.storage.all())
        
        self.assertEqual(final_count - initial_count, 1)
        
        # Verify object is in storage
        key = f"State.{state.id}"
        self.assertIn(key, self.storage.all())

    def test_file_storage_save_reload(self):
        """Test save and reload methods"""
        # Create and save objects
        state = State(name="Texas")
        city = City(name="Houston", state_id=state.id)
        
        self.storage.new(state)
        self.storage.new(city)
        
        # Save to file
        self.storage._FileStorage__file_path = self.test_file
        self.storage.save()
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_file))
        
        # Create new storage instance and reload
        new_storage = FileStorage()
        new_storage._FileStorage__file_path = self.test_file
        new_storage.reload()
        
        # Verify objects were reloaded
        all_objects = new_storage.all()
        state_key = f"State.{state.id}"
        city_key = f"City.{city.id}"
        
        self.assertIn(state_key, all_objects)
        self.assertIn(city_key, all_objects)
        
        # Verify object data
        reloaded_state = all_objects[state_key]
        reloaded_city = all_objects[city_key]
        
        self.assertEqual(reloaded_state.name, "Texas")
        self.assertEqual(reloaded_city.name, "Houston")
        self.assertEqual(reloaded_city.state_id, state.id)

    def test_file_storage_reload_nonexistent_file(self):
        """Test reload with nonexistent file"""
        self.storage._FileStorage__file_path = "nonexistent_file.json"
        
        # Should not raise exception
        try:
            self.storage.reload()
        except FileNotFoundError:
            self.fail("reload() raised FileNotFoundError unexpectedly!")

    def test_file_storage_delete(self):
        """Test delete method if implemented"""
        state = State(name="Nevada")
        self.storage.new(state)
        
        key = f"State.{state.id}"
        self.assertIn(key, self.storage.all())
        
        # Test delete if method exists
        if hasattr(self.storage, 'delete'):
            self.storage.delete(state)
            self.assertNotIn(key, self.storage.all())

    def test_file_storage_get(self):
        """Test get method if implemented"""
        state = State(name="Oregon")
        self.storage.new(state)
        
        if hasattr(self.storage, 'get'):
            retrieved_state = self.storage.get(State, state.id)
            self.assertEqual(retrieved_state.id, state.id)
            self.assertEqual(retrieved_state.name, "Oregon")
            
            # Test with nonexistent ID
            nonexistent = self.storage.get(State, "nonexistent-id")
            self.assertIsNone(nonexistent)

    def test_file_storage_count(self):
        """Test count method if implemented"""
        if hasattr(self.storage, 'count'):
            initial_count = self.storage.count()
            
            # Add some objects
            state1 = State(name="Idaho")
            state2 = State(name="Utah")
            city1 = City(name="Boise", state_id=state1.id)
            
            self.storage.new(state1)
            self.storage.new(state2)
            self.storage.new(city1)
            
            # Test total count
            final_count = self.storage.count()
            self.assertEqual(final_count - initial_count, 3)
            
            # Test count by class
            state_count = self.storage.count(State)
            city_count = self.storage.count(City)
            
            self.assertEqual(state_count, 2)
            self.assertEqual(city_count, 1)

    def test_file_storage_all_with_class(self):
        """Test all method with class parameter"""
        # Create objects of different classes
        state = State(name="Montana")
        user = User(email="test@test.com")
        
        self.storage.new(state)
        self.storage.new(user)
        
        # Test all with specific class
        all_states = self.storage.all(State)
        all_users = self.storage.all(User)
        
        # Should only contain objects of specified class
        for obj in all_states.values():
            self.assertIsInstance(obj, State)
        
        for obj in all_users.values():
            self.assertIsInstance(obj, User)
        
        # Verify correct objects are returned
        self.assertEqual(len(all_states), 1)
        self.assertEqual(len(all_users), 1)
        
        state_obj = list(all_states.values())[0]
        user_obj = list(all_users.values())[0]
        
        self.assertEqual(state_obj.name, "Montana")
        self.assertEqual(user_obj.email, "test@test.com")


if __name__ == '__main__':
    unittest.main()
