#!/usr/bin/python3
"""
Test suite for console.py create command with parameters
"""
import unittest
from io import StringIO
from unittest.mock import patch
import os
import sys

  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestConsoleCreateParams(unittest.TestCase):
    """Test create command with parameters"""
    
    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        
    def tearDown(self):
        """Clean up after tests"""
        
        storage._FileStorage__objects.clear()
        
    def test_create_no_class(self):
        """Test create with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(f.getvalue(), "** class name missing **\n")
    
    def test_create_invalid_class(self):
        """Test create with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create InvalidClass")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")
    
    def test_create_state_no_params(self):
        """Test create State without parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()
            self.assertTrue(len(state_id) > 0)
            
            key = "State.{}".format(state_id)
            self.assertIn(key, storage.all())
    
    def test_create_state_with_string_param(self):
        """Test create State with string parameter"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, "California")
    
    def test_create_state_with_underscore_replacement(self):
        """Test create State with underscores replaced by spaces"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="New_York"')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, "New York")
    
    def test_create_with_escaped_quotes(self):
        """Test create with escaped quotes in string"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="John\\"s_State"')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, 'John"s State')
    
    def test_create_place_with_multiple_params(self):
        """Test create Place with multiple parameters of different types"""
        cmd = ('create Place city_id="0001" user_id="0001" '
               'name="My_little_house" number_rooms=4 number_bathrooms=2 '
               'max_guest=10 price_by_night=300 latitude=37.773972 '
               'longitude=-122.431297')
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()
            key = "Place.{}".format(place_id)
            place = storage.all()[key]
            
            # Checking string values
            self.assertEqual(place.city_id, "0001")
            self.assertEqual(place.user_id, "0001")
            self.assertEqual(place.name, "My little house")
            
            # Checking integer values
            self.assertEqual(place.number_rooms, 4)
            self.assertEqual(place.number_bathrooms, 2)
            self.assertEqual(place.max_guest, 10)
            self.assertEqual(place.price_by_night, 300)
            
            # Checking float values
            self.assertEqual(place.latitude, 37.773972)
            self.assertEqual(place.longitude, -122.431297)
    
    def test_create_with_invalid_string_format(self):
        """Test create with invalid string format (no closing quote)"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            
            self.assertFalse(hasattr(state, 'name') and 
                           getattr(state, 'name') == "California")
    
    def test_create_with_invalid_number_format(self):
        """Test create with invalid number format"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place number_rooms=abc')
            place_id = f.getvalue().strip()
            key = "Place.{}".format(place_id)
            place = storage.all()[key]
            
            self.assertFalse(hasattr(place, 'number_rooms') and 
                           getattr(place, 'number_rooms') == 'abc')
    
    def test_create_with_empty_value(self):
        """Test create with empty parameter value"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name=')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
                     self.assertFalse(hasattr(state, 'name') and state.name == '')
    
    def test_create_with_no_equals_sign(self):
        """Test create with parameter without equals sign"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State California')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
                       self.assertIn(key, storage.all())
    
    def test_create_with_mixed_valid_invalid_params(self):
        """Test create with mix of valid and invalid parameters"""
        cmd = ('create Place name="Valid_House" invalid_param '
               'number_rooms=4 bad_float=12.ab latitude=37.77')
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()
            key = "Place.{}".format(place_id)
            place = storage.all()[key]
            
            
            self.assertEqual(place.name, "Valid House")
            self.assertEqual(place.number_rooms, 4)
            self.assertEqual(place.latitude, 37.77)
            
            
            self.assertFalse(hasattr(place, 'invalid_param'))
            self.assertFalse(hasattr(place, 'bad_float'))
    
    def test_parse_parameter_value_string(self):
        """Test _parse_parameter_value method for strings"""
        console = HBNBCommand()
        
        
        result = console._parse_parameter_value('"Hello World"')
        self.assertEqual(result, "Hello World")
        
        
        result = console._parse_parameter_value('"Hello_World"')
        self.assertEqual(result, "Hello World")
        
        
        result = console._parse_parameter_value('"He said \\"Hello\\""')
        self.assertEqual(result, 'He said "Hello"')
        
                result = console._parse_parameter_value('"Hello')
        self.assertIsNone(result)
    
    def test_parse_parameter_value_numbers(self):
        """Test _parse_parameter_value method for numbers"""
        console = HBNBCommand()
        
                result = console._parse_parameter_value('42')
        self.assertEqual(result, 42)
        
        
        result = console._parse_parameter_value('3.14')
        self.assertEqual(result, 3.14)
        
        
        result = console._parse_parameter_value('abc')
        self.assertIsNone(result)
        
         
        result = console._parse_parameter_value('12.34.56')
        self.assertIsNone(result)
    
    def test_create_user_with_params(self):
        """Test create User with various parameters"""
        cmd = 'create User email="test@example.com" password="secret123" first_name="John" last_name="Doe"'
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(cmd)
            user_id = f.getvalue().strip()
            key = "User.{}".format(user_id)
            user = storage.all()[key]
            
            self.assertEqual(user.email, "test@example.com")
            self.assertEqual(user.password, "secret123")
            self.assertEqual(user.first_name, "John")
            self.assertEqual(user.last_name, "Doe")


if __name__ == '__main__':
    unittest.main()
