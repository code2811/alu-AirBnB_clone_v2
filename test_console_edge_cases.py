#!/usr/bin/python3
"""
Additional edge case tests for console create functionality
"""
import unittest
from io import StringIO
from unittest.mock import patch
import os
import sys

# Add parent directory to path to import console
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from console import HBNBCommand
from models import storage


class TestConsoleCreateEdgeCases(unittest.TestCase):
    """Test edge cases for create command parameters"""
    
    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        
    def tearDown(self):
        """Clean up after tests"""
        storage._FileStorage__objects.clear()
    
    def test_create_with_multiple_equals_in_value(self):
        """Test parameter with multiple equals signs"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="equation=x=y"')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, "equation=x=y")
    
    def test_create_with_special_characters_in_string(self):
        """Test string with special characters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="State_with_@#$%_chars"')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, "State with @#$% chars")
    
    def test_create_with_empty_string(self):
        """Test parameter with empty string value"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name=""')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, "")
    
    def test_create_with_zero_values(self):
        """Test parameters with zero values"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place number_rooms=0 latitude=0.0 price_by_night=0')
            place_id = f.getvalue().strip()
            key = "Place.{}".format(place_id)
            place = storage.all()[key]
            
            self.assertEqual(place.number_rooms, 0)
            self.assertEqual(place.latitude, 0.0)
            self.assertEqual(place.price_by_night, 0)
    
    def test_create_with_negative_numbers(self):
        """Test parameters with negative numbers"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place latitude=-37.773972 price_by_night=-100')
            place_id = f.getvalue().strip()
            key = "Place.{}".format(place_id)
            place = storage.all()[key]
            
            self.assertEqual(place.latitude, -37.773972)
            self.assertEqual(place.price_by_night, -100)
    
    def test_create_with_very_long_string(self):
        """Test parameter with very long string"""
        long_name = "Very_" * 100 + "Long_Name"
        expected_name = "Very " * 100 + "Long Name"
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'create State name="{long_name}"')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, expected_name)
    
    def test_create_with_unicode_characters(self):
        """Test string with unicode characters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="Cañon_City_México"')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, "Cañon City México")
    
    def test_create_with_only_quotes_string(self):
        """Test string that is only quotes"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="\\"\\"\\""')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, '"""')
    
    def test_create_with_scientific_notation(self):
        """Test float in scientific notation"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place latitude=1.23e-4')
            place_id = f.getvalue().strip()
            key = "Place.{}".format(place_id)
            place = storage.all()[key]
            self.assertEqual(place.latitude, 1.23e-4)
    
    def test_create_with_leading_trailing_spaces_in_key(self):
        """Test parameter key with leading/trailing spaces (should work)"""
        with patch('sys.stdout', new=StringIO()) as f:
            # Note: spaces around key should be handled by split()
            self.console.onecmd('create State  name="California"  ')
            state_id = f.getvalue().strip()
            key = "State.{}".format(state_id)
            state = storage.all()[key]
            self.assertEqual(state.name, "California")


if __name__ == '__main__':
    unittest.main()
