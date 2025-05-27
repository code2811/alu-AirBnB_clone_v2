import unittest
import os
import MySQLdb
from models import storage
from models.amenity import Amenity
from models.place_amenity import PlaceAmenity

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Tests for DB storage only")
class TestAmenityDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup DB connection and cursor once for all tests"""
        cls.mysql_user = os.getenv('HBNB_MYSQL_USER', 'hbnb_test')
        cls.mysql_pwd = os.getenv('HBNB_MYSQL_PWD', 'hbnb_test_pwd')
        cls.mysql_host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        cls.mysql_db = os.getenv('HBNB_MYSQL_DB', 'hbnb_test_db')

        cls.db = MySQLdb.connect(
            user=cls.mysql_user,
            passwd=cls.mysql_pwd,
            host=cls.mysql_host,
            db=cls.mysql_db
        )
        cls.cursor = cls.db.cursor()

    @classmethod
    def tearDownClass(cls):
        """Close DB connection after all tests"""
        cls.cursor.close()
        cls.db.close()

    def test_files_exist(self):
        """Test modules can be imported"""
        try:
            import models.amenity
            import models.place_amenity
        except ImportError:
            self.fail("Required model modules are missing")

    def test_tables_exist(self):
        """Test 'amenities' and 'place_amenity' tables exist"""
        self.cursor.execute("SHOW TABLES LIKE 'amenities'")
        self.assertIsNotNone(self.cursor.fetchone(), "Table 'amenities' not found")

        self.cursor.execute("SHOW TABLES LIKE 'place_amenity'")
        self.assertIsNotNone(self.cursor.fetchone(), "Table 'place_amenity' not found")

    def test_create_amenity_with_name(self):
        """Test creating Amenity with a name stores record in DB"""
        a = Amenity(name="Wifi")
        a.save()
        self.cursor.execute("SELECT * FROM amenities WHERE id=%s", (a.id,))
        row = self.cursor.fetchone()
        self.assertIsNotNone(row, "Amenity was not saved to DB")

        # Clean up
        self.cursor.execute("DELETE FROM amenities WHERE id=%s", (a.id,))
        self.db.commit()

    def test_create_amenity_without_name(self):
        """Test creating Amenity without name raises error or is prevented"""
        a = Amenity()
        with self.assertRaises(Exception):
            a.save()

    def test_list_amenities_from_db(self):
        """Test listing all amenities from DB returns at least one record"""
        self.cursor.execute("SELECT * FROM amenities")
        rows = self.cursor.fetchall()
        self.assertGreater(len(rows), 0, "No amenities found in DB")

    def test_create_place_amenity(self):
        """Test creating PlaceAmenity with existing place_id and amenity_id"""
        # For the test, fetch one place_id and one amenity_id from DB
        self.cursor.execute("SELECT id FROM places LIMIT 1")
        place = self.cursor.fetchone()
        self.cursor.execute("SELECT id FROM amenities LIMIT 1")
        amenity = self.cursor.fetchone()
        self.assertIsNotNone(place, "No place found in DB to use for PlaceAmenity test")
        self.assertIsNotNone(amenity, "No amenity found in DB to use for PlaceAmenity test")

        pa = PlaceAmenity(place_id=place[0], amenity_id=amenity[0])
        pa.save()

        self.cursor.execute(
            "SELECT * FROM place_amenity WHERE place_id=%s AND amenity_id=%s",
            (place[0], amenity[0])
        )
        row = self.cursor.fetchone()
        self.assertIsNotNone(row, "PlaceAmenity was not saved to DB")

        # Clean up
        self.cursor.execute(
            "DELETE FROM place_amenity WHERE place_id=%s AND amenity_id=%s",
            (place[0], amenity[0])
        )
        self.db.commit()

    def test_list_place_amenities_from_db(self):
        """Test listing all place_amenity entries returns at least one record"""
        self.cursor.execute("SELECT * FROM place_amenity")
        rows = self.cursor.fetchall()
        self.assertGreater(len(rows), 0, "No place_amenity records found in DB")

if __name__ == '__main__':
    unittest.main()

