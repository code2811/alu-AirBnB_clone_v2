#!/usr/bin/python3
"""Unittest to test DB command create with console"""
import unittest
import MySQLdb
import os
from io import StringIO
from contextlib import redirect_stdout
from console import HBNBCommand

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Only for DBStorage")
class TestConsoleDBCreate(unittest.TestCase):
    def setUp(self):
        """Set up DB connection"""
        self.db = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        self.cursor = self.db.cursor()

    def tearDown(self):
        """Close DB connection"""
        self.cursor.close()
        self.db.close()

    def test_create_state_adds_row(self):
        """Test that 'create State name="California"' adds a row"""
        # Count states before
        self.cursor.execute("SELECT COUNT(*) FROM states;")
        before = self.cursor.fetchone()[0]

        # Run console command
        with redirect_stdout(StringIO()):
            HBNBCommand().onecmd('create State name="California"')

        # Count states after
        self.cursor.execute("SELECT COUNT(*) FROM states;")
        after = self.cursor.fetchone()[0]

        self.assertEqual(after, before + 1)

