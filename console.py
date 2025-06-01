#!/usr/bin/python3
"""Test cases for console module"""

import unittest
import os
import MySQLdb
from console import HBNBCommand
from models import storage
from models.state import State
from models.city import City
from io import StringIO
import sys


class TestConsole(unittest.TestCase):
    """Test console commands"""
    
    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
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

    def create_and_capture_output(self, command):
        """Helper method to capture console output"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        self.console.onecmd(command)
        
        output = captured_output.getvalue().strip()
        sys.stdout = old_stdout
        return output

    def test_help_command(self):
        """Test help command - works with both storage types"""
        output = self.create_and_capture_output("help")
        self.assertIn("Documented commands", output)

    def test_create_command_basic(self):
        """Test basic create command - works with both storage types"""
        output = self.create_and_capture_output("create State")
        self.assertTrue(len(output) > 0)  # Should return an ID

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Skip for non-database storage")
    def test_create_state_with_name_db(self):
        """Test creating state with name parameter in database"""
        # Get initial count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]
        
        # Create state with name
        output = self.create_and_capture_output('create State name="California"')
        state_id = output
        
        # Check database count increased
        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchone()[0]
        self.assertEqual(new_count, initial_count + 1)
        
        # Verify the state exists with correct name
        self.cursor.execute("SELECT name FROM states WHERE id = %s", (state_id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "California")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 
                     "Skip for database storage")
    def test_create_state_file_storage(self):
        """Test creating state in file storage"""
        output = self.create_and_capture_output("create State")
        state_id = output
        
        # Check if object is in storage
        key = f"State.{state_id}"
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Skip for non-database storage")
    def test_create_city_with_state_id_db(self):
        """Test creating city with state_id in database"""
        # First create a state
        state_output = self.create_and_capture_output('create State name="Texas"')
        state_id = state_output
        
        # Get initial city count
        self.cursor.execute("SELECT COUNT(*) FROM cities")
        initial_count = self.cursor.fetchone()[0]
        
        # Create city with state_id
        city_output = self.create_and_capture_output(
            f'create City state_id="{state_id}" name="Houston"'
        )
        city_id = city_output
        
        # Check database count increased
        self.cursor.execute("SELECT COUNT(*) FROM cities")
        new_count = self.cursor.fetchone()[0]
        self.assertEqual(new_count, initial_count + 1)
        
        # Verify the city exists with correct state_id and name
        self.cursor.execute(
            "SELECT name, state_id FROM cities WHERE id = %s", (city_id,)
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Houston")
        self.assertEqual(result[1], state_id)

    def test_show_command(self):
        """Test show command - works with both storage types"""
        # Create a state first
        create_output = self.create_and_capture_output("create State")
        state_id = create_output
        
        # Show the state
        show_output = self.create_and_capture_output(f"show State {state_id}")
        self.assertIn(state_id, show_output)
        self.assertIn("State", show_output)

    def test_destroy_command(self):
        """Test destroy command - works with both storage types"""
        # Create a state first
        create_output = self.create_and_capture_output("create State")
        state_id = create_output
        
        # Destroy the state
        self.create_and_capture_output(f"destroy State {state_id}")
        
        # Try to show the destroyed state (should not exist)
        show_output = self.create_and_capture_output(f"show State {state_id}")
        self.assertIn("** no instance found **", show_output)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Skip for non-database storage")
    def test_destroy_command_db_verification(self):
        """Test destroy command with database verification"""
        # Create a state
        create_output = self.create_and_capture_output('create State name="ToDestroy"')
        state_id = create_output
        
        # Verify it exists in database
        self.cursor.execute("SELECT COUNT(*) FROM states WHERE id = %s", (state_id,))
        count_before = self.cursor.fetchone()[0]
        self.assertEqual(count_before, 1)
        
        # Destroy the state
        self.create_and_capture_output(f"destroy State {state_id}")
        
        # Verify it's gone from database
        self.cursor.execute("SELECT COUNT(*) FROM states WHERE id = %s", (state_id,))
        count_after = self.cursor.fetchone()[0]
        self.assertEqual(count_after, 0)

    def test_all_command(self):
        """Test all command - works with both storage types"""
        # Create a few states
        self.create_and_capture_output("create State")
        self.create_and_capture_output("create State")
        
        # Get all states
        all_output = self.create_and_capture_output("all State")
        self.assertIn("State", all_output)

    def test_update_command(self):
        """Test update command - works with both storage types"""
        # Create a state
        create_output = self.create_and_capture_output("create State")
        state_id = create_output
        
        # Update the state
        self.create_and_capture_output(f'update State {state_id} name "Updated"')
        
        # Show the updated state
        show_output = self.create_and_capture_output(f"show State {state_id}")
        self.assertIn("Updated", show_output)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Skip for non-database storage")
    def test_update_command_db_verification(self):
        """Test update command with database verification"""
        # Create a state
        create_output = self.create_and_capture_output('create State name="Original"')
        state_id = create_output
        
        # Update the state
        self.create_and_capture_output(f'update State {state_id} name "Updated"')
        
        # Verify update in database
        self.cursor.execute("SELECT name FROM states WHERE id = %s", (state_id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Updated")


if __name__ == '__main__':
    unittest.main()
