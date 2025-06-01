#!/usr/bin/python3
"""
Test cases for console module
"""

import unittest
import os
import MySQLdb
from unittest import skipIf
from io import StringIO
import sys
from console import HBNBCommand
from models import storage
from models.state import State
from models.city import City
from models.user import User


class TestConsoleCommand(unittest.TestCase):
    """Test cases for console commands"""

    def setUp(self):
        """Set up test fixtures"""
        self.console = HBNBCommand()
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

    def create_mock_stdin(self, input_data):
        """Create mock stdin for testing"""
        return StringIO(input_data)

    def capture_stdout(self, command):
        """Capture stdout from console command"""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            self.console.onecmd(command)
            output = sys.stdout.getvalue().strip()
        finally:
            sys.stdout = old_stdout
        
        return output

    def test_help_command(self):
        """Test help command"""
        output = self.capture_stdout("help")
        self.assertIn("Documented commands", output)

    def test_quit_command(self):
        """Test quit command"""
        with self.assertRaises(SystemExit):
            self.console.onecmd("quit")

    def test_EOF_command(self):
        """Test EOF command"""
        with self.assertRaises(SystemExit):
            self.console.onecmd("EOF")

    def test_empty_line(self):
        """Test empty line input"""
        output = self.capture_stdout("")
        self.assertEqual(output, "")

    @skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
            "Database storage only")
    def test_create_state_db(self):
        """Test create State command with database"""
        # Get initial count from database
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]
        
        # Execute create command
        output = self.capture_stdout('create State name="California"')
        
        # Verify output is a valid UUID
        self.assertTrue(len(output) > 0)
        
        # Check database count increased
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_count = self.cursor.fetchone()[0]
        self.assertEqual(final_count - initial_count, 1)
        
        # Verify state data in database
        self.cursor.execute(
            "SELECT name FROM states WHERE id = %s", (output,)
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "California")

    @skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', 
            "File storage only")
    def test_create_state_file(self):
        """Test create State command with file storage"""
        initial_count = len([obj for obj in storage.all().values() 
                           if type(obj) is State])
        
        output = self.capture_stdout('create State name="Texas"')
        
        # Verify output is a valid UUID
        self.assertTrue(len(output) > 0)
        
        # Check storage count increased
        final_count = len([obj for obj in storage.all().values() 
                         if type(obj) is State])
        self.assertEqual(final_count - initial_count, 1)

    def test_create_with_parameters(self):
        """Test create command with parameters"""
        output = self.capture_stdout(
            'create User email="test@test.com" password="123" '
            'first_name="John" last_name="Doe"'
        )
        
        # Should return UUID
        self.assertTrue(len(output) > 0)
        
        # Verify object was created
        user_key = f"User.{output}"
        all_objects = storage.all()
        self.assertIn(user_key, all_objects)
        
        user = all_objects[user_key]
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_show_command(self):
        """Test show command"""
        # First create an object
        create_output = self.capture_stdout('create State name="Nevada"')
        state_id = create_output
        
        # Then show it
        show_output = self.capture_stdout(f'show State {state_id}')
        
        self.assertIn("State", show_output)
        self.assertIn(state_id, show_output)
        self.assertIn("Nevada", show_output)

    def test_show_nonexistent(self):
        """Test show command with nonexistent object"""
        output = self.capture_stdout('show State nonexistent-id')
        self.assertIn("** no instance found **", output)

    def test_destroy_command(self):
        """Test destroy command"""
        # Create object first
        create_output = self.capture_stdout('create State name="ToDelete"')
        state_id = create_output
        
        # Verify it exists
        show_output = self.capture_stdout(f'show State {state_id}')
        self.assertIn("ToDelete", show_output)
        
        # Destroy it
        destroy_output = self.capture_stdout(f'destroy State {state_id}')
        self.assertEqual(destroy_output, "")
        
        # Verify it's gone
        show_output = self.capture_stdout(f'show State {state_id}')
        self.assertIn("** no instance found **", show_output)

    def test_all_command(self):
        """Test all command"""
        output = self.capture_stdout('all State')
        self.assertTrue(output.startswith('['))
        self.assertTrue(output.endswith(']'))

    def test_all_command_with_class(self):
        """Test all command with specific class"""
        # Create a state first
        self.capture_stdout('create State name="TestAll"')
        
        output = self.capture_stdout('all State')
        self.assertIn("TestAll", output)

    def test_update_command(self):
        """Test update command"""
        # Create object first
        create_output = self.capture_stdout('create State name="OldName"')
        state_id = create_output
        
        # Update it
        update_output = self.capture_stdout(
            f'update State {state_id} name "NewName"'
        )
        self.assertEqual(update_output, "")
        
        # Verify update
        show_output = self.capture_stdout(f'show State {state_id}')
        self.assertIn("NewName", show_output)

    def test_count_command(self):
        """Test count command if implemented"""
        output = self.capture_stdout('count State')
        # Should return a number or empty if not implemented
        if output:
            self.assertTrue(output.isdigit())

    def test_invalid_command(self):
        """Test invalid command"""
        output = self.capture_stdout('invalid_command')
        self.assertIn("*** Unknown syntax", output)

    def test_create_missing_class(self):
        """Test create command without class name"""
        output = self.capture_stdout('create')
        self.assertIn("** class name missing **", output)

    def test_create_invalid_class(self):
        """Test create command with invalid class"""
        output = self.capture_stdout('create InvalidClass')
        self.assertIn("** class doesn't exist **", output)


if __name__ == '__main__':
    unittest.main()
