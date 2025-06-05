#!/usr/bin/env python3
"""
Comprehensive test suite for AirBnB Clone v2 - PEP8 compliant
File: tests/test_console.py
"""

import unittest
import os
import MySQLdb
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class TestConsoleFileStorage(unittest.TestCase):
    """Test console with file storage"""

    def setUp(self):
        """Set up test environment"""
        self.storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')

    def tearDown(self):
        """Clean up after tests"""
        if self.storage_type == 'file':
            try:
                os.remove("file.json")
            except FileNotFoundError:
                pass

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_create_state_file_storage(self):
        """Test create State with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California"')
            state_id = f.getvalue().strip()
        self.assertTrue(state_id)
        key = "State.{}".format(state_id)
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_create_city_file_storage(self):
        """Test create City with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Nevada"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Las_Vegas"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()
        key = "City.{}".format(city_id)
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_create_user_file_storage(self):
        """Test create User with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="test@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()
        key = "User.{}".format(user_id)
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_create_place_file_storage(self):
        """Test create Place with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Texas"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Dallas"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="user@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Place city_id="{}" user_id="{}" name="House"'.format(
                city_id, user_id)
            HBNBCommand().onecmd(cmd)
            place_id = f.getvalue().strip()
        key = "Place.{}".format(place_id)
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_create_review_file_storage(self):
        """Test create Review with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Florida"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Miami"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="owner@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Place city_id="{}" user_id="{}" name="Villa"'.format(
                city_id, user_id)
            HBNBCommand().onecmd(cmd)
            place_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Review place_id="{}" user_id="{}" text="Great"'.format(
                place_id, user_id)
            HBNBCommand().onecmd(cmd)
            review_id = f.getvalue().strip()
        key = "Review.{}".format(review_id)
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_create_amenity_file_storage(self):
        """Test create Amenity with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity name="WiFi"')
            amenity_id = f.getvalue().strip()
        key = "Amenity.{}".format(amenity_id)
        self.assertIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_show_command_file_storage(self):
        """Test show command with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Ohio"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show State {}'.format(state_id))
            output = f.getvalue().strip()
        self.assertIn(state_id, output)
        self.assertIn("Ohio", output)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_all_command_file_storage(self):
        """Test all command with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Michigan"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all State')
            output = f.getvalue().strip()
        self.assertIn("Michigan", output)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_destroy_command_file_storage(self):
        """Test destroy command with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Georgia"')
            state_id = f.getvalue().strip()
        key = "State.{}".format(state_id)
        self.assertIn(key, storage.all())
        HBNBCommand().onecmd('destroy State {}'.format(state_id))
        self.assertNotIn(key, storage.all())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_update_command_file_storage(self):
        """Test update command with file storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Oregon"')
            state_id = f.getvalue().strip()
        cmd = 'update State {} name "Washington"'.format(state_id)
        HBNBCommand().onecmd(cmd)
        key = "State.{}".format(state_id)
        state = storage.all()[key]
        self.assertEqual(state.name, "Washington")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_count_command_file_storage(self):
        """Test count command with file storage"""
        initial_count = len([obj for obj in storage.all().values()
                            if type(obj).__name__ == "State"])
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Idaho"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('count State')
            output = f.getvalue().strip()
        self.assertEqual(int(output), initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_parameter_parsing_strings(self):
        """Test parameter parsing with strings"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="New_York"')
            state_id = f.getvalue().strip()
        key = "State.{}".format(state_id)
        state = storage.all()[key]
        self.assertEqual(state.name, "New York")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_parameter_parsing_integers(self):
        """Test parameter parsing with integers"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Test"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Test"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="test@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = ('create Place city_id="{}" user_id="{}" name="Test" '
                   'number_rooms=4 max_guest=8 price_by_night=100').format(
                city_id, user_id)
            HBNBCommand().onecmd(cmd)
            place_id = f.getvalue().strip()
        key = "Place.{}".format(place_id)
        place = storage.all()[key]
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.max_guest, 8)
        self.assertEqual(place.price_by_night, 100)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Skip file storage tests")
    def test_parameter_parsing_floats(self):
        """Test parameter parsing with floats"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Test"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Test"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="test@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = ('create Place city_id="{}" user_id="{}" name="Test" '
                   'latitude=37.774 longitude=-122.431').format(
                city_id, user_id)
            HBNBCommand().onecmd(cmd)
            place_id = f.getvalue().strip()
        key = "Place.{}".format(place_id)
        place = storage.all()[key]
        self.assertAlmostEqual(place.latitude, 37.774)
        self.assertAlmostEqual(place.longitude, -122.431)


class TestConsoleDBStorage(unittest.TestCase):
    """Test console with database storage"""

    def setUp(self):
        """Set up test environment"""
        self.storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')

    def get_db_connection(self):
        """Get direct MySQL connection"""
        return MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER', 'hbnb_test'),
            passwd=os.getenv('HBNB_MYSQL_PWD', 'hbnb_test_pwd'),
            db=os.getenv('HBNB_MYSQL_DB', 'hbnb_test_db')
        )

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_create_state_db_storage(self):
        """Test create State with database storage"""
        db = self.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = cursor.fetchone()[0]
        cursor.close()

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California"')
            state_id = f.getvalue().strip()

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        new_count = cursor.fetchone()[0]
        cursor.close()
        db.close()

        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_create_city_db_storage(self):
        """Test create City with database storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Texas"')
            state_id = f.getvalue().strip()

        db = self.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities")
        initial_count = cursor.fetchone()[0]
        cursor.close()

        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Dallas"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM cities")
        new_count = cursor.fetchone()[0]
        cursor.close()
        db.close()

        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_create_user_db_storage(self):
        """Test create User with database storage"""
        db = self.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        initial_count = cursor.fetchone()[0]
        cursor.close()

        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="test@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        new_count = cursor.fetchone()[0]
        cursor.close()
        db.close()

        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_create_place_db_storage(self):
        """Test create Place with database storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Florida"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Miami"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="owner@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()

        db = self.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM places")
        initial_count = cursor.fetchone()[0]
        cursor.close()

        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Place city_id="{}" user_id="{}" name="Villa"'.format(
                city_id, user_id)
            HBNBCommand().onecmd(cmd)
            place_id = f.getvalue().strip()

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM places")
        new_count = cursor.fetchone()[0]
        cursor.close()
        db.close()

        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_create_review_db_storage(self):
        """Test create Review with database storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Nevada"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create City state_id="{}" name="Vegas"'.format(state_id)
            HBNBCommand().onecmd(cmd)
            city_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create User email="guest@test.com" password="pwd"'
            HBNBCommand().onecmd(cmd)
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Place city_id="{}" user_id="{}" name="Hotel"'.format(
                city_id, user_id)
            HBNBCommand().onecmd(cmd)
            place_id = f.getvalue().strip()

        db = self.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM reviews")
        initial_count = cursor.fetchone()[0]
        cursor.close()

        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Review place_id="{}" user_id="{}" text="Good"'.format(
                place_id, user_id)
            HBNBCommand().onecmd(cmd)
            review_id = f.getvalue().strip()

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM reviews")
        new_count = cursor.fetchone()[0]
        cursor.close()
        db.close()

        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_create_amenity_db_storage(self):
        """Test create Amenity with database storage"""
        db = self.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM amenities")
        initial_count = cursor.fetchone()[0]
        cursor.close()

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Amenity name="Pool"')
            amenity_id = f.getvalue().strip()

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM amenities")
        new_count = cursor.fetchone()[0]
        cursor.close()
        db.close()

        self.assertEqual(new_count, initial_count + 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_show_command_db_storage(self):
        """Test show command with database storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Ohio"')
            state_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show State {}'.format(state_id))
            output = f.getvalue().strip()
        self.assertIn(state_id, output)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_all_command_db_storage(self):
        """Test all command with database storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Michigan"')
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all State')
            output = f.getvalue().strip()
        self.assertIn("Michigan", output)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Skip database tests")
    def test_destroy_command_db_storage(self):
        """Test destroy command with database storage"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="Georgia"')
            state_id = f.getvalue().strip()

        db = self.get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM states WHERE id = %s",
                       (state_id,))
        count_before = cursor.fetchone()[0]
        cursor.close()

        HBNBCommand().onecmd('destroy State {}'.format(state_id))

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM states WHERE id = %s",
                       (state_id,))
        count_after = cursor.fetchone()[0]
        cursor.close()
        db.close()

        self.assertEqual(count_before, 1)
        self.assertEqual(count_after, 0)


if __name__ == '__main__':
    unittest.main()
