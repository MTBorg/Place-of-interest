import unittest
import db as database
import logging
import json
import psycopg2
import datetime
from psycopg2.extensions import AsIs

from setup import createDatabase, createDBUser, createTables, grantDBUser

# WARNING: DO NOT remove or edit points (unless you really know what you are doing) as this will most likely break already implemented tests.
# Instead just add new ones.
points = [
    {"marker": (0,0), "ip_address": "123.123.123.123", "user_id": "0"},
    {"marker": (1,1), "ip_address": "123.123.123.123", "user_id": "0"},
    {"marker": (100,80), "ip_address": "192.168.10.34", "user_id": "1"},
    {"marker": (-10,0), "ip_address": "123.123.123.123", "user_id": "2"},
    {"marker": (22.1509272,65.5857114), "ip_address": "234.234.234.234", "user_id": "3"}, # Kulturens hus, Luleå
    {"marker": (22.1339231,65.6181932), "ip_address": "234.234.234.234", "user_id": "3"} # Aula Aurora, Luleå University of Technology, Luleå
]

class dbTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            logging.info("Reading configuration file test_conf.json")
            with open('testConf.json') as f:
                conf = json.load(f)
                cls.test_user = conf["poi_user"]
                cls.test_db = conf["poi_db"]
                cls.superuser = conf["superuser"]
                cls.connection = conf["connection"]

                # Connect to the default database
                db_connection = psycopg2.connect(
                    dbname = "postgres",
                    user = cls.superuser["name"],
                    password = cls.superuser["password"],
                    host = cls.connection["host"],
                    port = cls.connection["port"]
                )
                db_connection.autocommit = True
                cls.db_cursor = db_connection.cursor()

                cls.drop_table()
                cls.drop_user()

                #Create database user
                logging.info("Setting up test user %s", cls.test_user["name"])
                createDBUser.create_dbuser(
                    host_name = cls.connection["host"],
                    host_port = cls.connection["port"],
                    psql_pass = cls.superuser["password"],
                    dbuser_name = cls.test_user["name"],
                    dbuser_pass = cls.test_user["password"]
                )

                #Create database
                logging.info("Setting up test database %s", cls.test_db["name"])
                createDatabase.create_database(
                    host_name = cls.connection["host"],
                    host_port = cls.connection["port"],
                    psql_pass = cls.superuser["password"],
                    db_name = cls.test_db["name"],
                    db_owner = cls.superuser["name"]
                )

                #Create tables
                logging.info("Setting up tables")
                createTables.create_tables(
                    dbname = cls.test_db["name"],
                    username = cls.superuser["name"],
                    hostname = cls.connection["host"],
                    password = cls.superuser["password"],
                    portnr = cls.connection["port"]
                )

                # Give the database user grants
                logging.info("Giving user %s grants", cls.test_user["name"])
                grantDBUser.grant_dbuser(
                    db_name = cls.test_db["name"],
                    dbuser_name = cls.test_user["name"],
                    host_name = cls.connection["host"],
                    host_port = cls.connection["port"],
                    psql_pass = cls.superuser["password"]
                )

                #Insert test points
                logging.info("Connecting to database %s to insert points", cls.test_db["name"])
                db = database.db("../testConf.json") # NOTE: The path is relative to the db file
                logging.info("Inserting %s points", len(points))
                for point in points:
                    db.save_marker(
                        lng = point["marker"][0],
                        lat = point["marker"][1],
                        ip_address = point["ip_address"],
                        user_id = point["user_id"]
                    )
                logging.info("Test database %s was successfully setup", cls.test_db["name"])
        except:
            logging.exception("Unknown exception")


    @classmethod
    def drop_table(cls):
        # Drop the database
        logging.info("Dropping database %s after all tests", cls.test_db["name"])
        try:
            cls.db_cursor.execute("DROP DATABASE %s;", (AsIs(cls.test_db["name"]),))
        except psycopg2.Error as e:
            if (e.pgcode == '3D000'): # invalid_catalog_name error code
                logging.info("Could not find database %s, continuing...", cls.test_db["name"])
            else:
                raise


    @classmethod
    def drop_user(cls):
        # Drop the user
        logging.info("Dropping user %s in after all tests", cls.test_user["name"])
        try:    
            cls.db_cursor.execute("DROP ROLE %s;", (AsIs(cls.test_user["name"]),))
        except psycopg2.ProgrammingError as e:
            if (e.pgcode == '42704'): # undefined_object error code
                logging.info("Could not find user %s, continuing...", cls.test_user["name"])
            else:
                raise


    @classmethod
    def tearDownClass(cls):
        cls.drop_table()
        cls.drop_user()

    def test_get_markers_from_userid(self):
        logging.info("Testing getting markers from user id")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        # Check that the function returns a list
        self.assertIsInstance([], type(db.get_markers_from_userid("0")))

        self.assertIn((0.0,0.0), db.get_markers_from_userid("0"))
        self.assertIn((0,0), db.get_markers_from_userid("0"))
        self.assertIn((100, 80), db.get_markers_from_userid("1"))
        self.assertIn((-10,0), db.get_markers_from_userid("2"))

        # May fail if additional points are added
        self.assertNotIn((100, 80), db.get_markers_from_userid("0"))
        self.assertNotIn((80,100), db.get_markers_from_userid("1"))
        self.assertNotIn((10,0), db.get_markers_from_userid("2"))
        self.assertNotIn((0.001,0.001), db.get_markers_from_userid("0"))
        self.assertNotIn((0.001,0.001), db.get_markers_from_userid("66"))
        self.assertEqual(len(db.get_markers_from_userid("66")), 0)
        self.assertEqual(len(db.get_markers_from_userid("454312")), 0)

    def test_get_markers_from_ip(self):
        logging.info("Testing getting markers from ip")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file
       
        # Check that the function returns a list
        self.assertIsInstance([], type(db.get_markers_from_userid("123.123.123.123")))

        #TODO: check multipte values in list?
        self.assertIn((0,0), db.get_markers_from_ip("123.123.123.123"))
        self.assertIn((-10,0), db.get_markers_from_ip("123.123.123.123"))
        self.assertIn((100,80), db.get_markers_from_ip("192.168.10.34"))
        
        # May fail if additional points are added
        self.assertNotIn((0,0), db.get_markers_from_ip("192.168.10.34"))
        self.assertNotIn((80,100), db.get_markers_from_ip("192.168.10.34"))
        self.assertNotIn((100.0001,80.001), db.get_markers_from_ip("192.168.10.34"))
        self.assertNotIn((100.0001,80.001), db.get_markers_from_ip("77"))
        self.assertEqual(len(db.get_markers_from_ip("77")), 0)
    
    def test_get_markers_from_userid_and_ip(self):
        logging.info("Testing getting markers from user id and ip")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        # Check that the function returns a list
        self.assertIsInstance([], type(db.get_markers_from_userid_and_ip("0", "123.123.123.123")))

        #TODO: check multipte values in list?
        self.assertIn((0,0), db.get_markers_from_userid_and_ip("0", "123.123.123.123"))
        self.assertIn((1,1), db.get_markers_from_userid_and_ip("0", "123.123.123.123"))
        self.assertIn((100,80), db.get_markers_from_userid_and_ip("1", "192.168.10.34"))
        self.assertIn((-10,0), db.get_markers_from_userid_and_ip("2", "123.123.123.123"))

        # May fail if additional points are added
        self.assertNotIn((80,100), db.get_markers_from_userid_and_ip("1", "192.168.10.34"))
        self.assertNotIn((10,0), db.get_markers_from_userid_and_ip("2", "123.123.123.123"))
        self.assertNotIn((10,0), db.get_markers_from_userid_and_ip("66", "77"))
        self.assertEqual(len(db.get_markers_from_userid_and_ip("66","77")), 0)
    
    def test_get_markers_from_dist(self):
        logging.info("Testing getting markers from distance")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        # Get all markers within a distance of 40080km (earth's circumference~=40075km) from (0,0), which should return all points
        self.assertEqual(len(points), len(db.get_markers_from_dist(0,0,40075000)))

        # Check that the function returns a list
        self.assertIsInstance([], type(db.get_markers_from_dist(0,0, 40075000)))

        # Tests between kulturens hus, Luleå and the roundabout outside ~= 87m
        self.assertIn((22.1509272,65.5857114), db.get_markers_from_dist(22.150144,65.5857025, 100))
        self.assertNotIn((22.1509272,65.5857114), db.get_markers_from_dist(22.150144,65.5857025, 30))

        # Tests between Aula Aurora, Luleå and Luleå train station, distance: ~4.06km
        self.assertIn((22.1339231,65.6181932), db.get_markers_from_dist(22.1627801,65.5839882, 4100))
        self.assertNotIn((22.1339231,65.6181932), db.get_markers_from_dist(22.1627801,65.5839882, 4000))

    def test_get_markers_from_dist_time(self):
        logging.info("Testing getting markers from distance and time")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        now = datetime.datetime.now() 
        yesterday = now - datetime.timedelta(days = 1)

        # Get all markers within a distance of 40080km (earth's circumference~=40075km) from (0,0), and between the earliest time possible to now, which should return all points
        self.assertEqual(len(points), len(db.get_markers_from_dist_time(0,0,40076000, datetime.date.min, now)))

        # Check that the function returns a list
        self.assertIsInstance([], type(db.get_markers_from_dist_time(0,0,40076000, datetime.date.min, now)))

        # Tests between kulturens hus, Luleå and the roundabout outside ~= 87m, inserted within last 24 hours
        self.assertIn((22.1509272,65.5857114), db.get_markers_from_dist_time(22.150144,65.5857025, 100, yesterday, now))
        self.assertNotIn((22.1509272,65.5857114), db.get_markers_from_dist_time(22.150144,65.5857025, 30, yesterday, now))

        # Tests between Aula Aurora, Luleå and Luleå train station, distance: ~4.06km, inserted within the last 24 hours
        self.assertIn((22.1339231,65.6181932), db.get_markers_from_dist_time(22.1627801,65.5839882, 4100, yesterday, now))
        self.assertNotIn((22.1339231,65.6181932), db.get_markers_from_dist_time(22.1627801,65.5839882, 4000, yesterday, now))

        # Tests between kulturens hus, Luleå and the roundabout outside ~= 87m, inserted in the last hour
        lasthour = now - datetime.timedelta(hours = 1)
        self.assertIn((22.1509272,65.5857114), db.get_markers_from_dist_time(22.150144,65.5857025, 100, lasthour, now))

        # Tests between kulturens hus, Luleå and the roundabout outside, inserted yesterday
        self.assertNotIn((22.1511663,65.58544844), db.get_markers_from_dist_time(22.1509888,65.5856349, 100, yesterday - datetime.timedelta(days=1), yesterday))

    def test_save_marker(self):
        logging.info("Testing saving marker")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        # Testing valid input format
        self.assertTrue(db.save_marker(0.0, 0.0, "ip_address", "user_id"))
        self.assertTrue(db.save_marker("0.0", 0.0, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(0.0, "0.0", "ip_address", "user_id"))
        self.assertTrue(db.save_marker(0.0, 0.0, 0, "user_id"))
        self.assertTrue(db.save_marker(0.0, 0.0, "ip_address", 0))
        self.assertTrue(db.save_marker(0.0, 0.0, 11, "user_id"))
        self.assertTrue(db.save_marker(0.0, 0.0, "ip_address", 11))

        # Testing random values for lng and lat
        self.assertTrue(db.save_marker(1, 2.2222222222, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(1.1111111111, 2, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(100, 1, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(1, 100, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(500, 1, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(1, 500, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(9999999999, 1, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(1, 9999999999, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(9999999999, 9999999999, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(-9999999999, -9999999999, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(10, 10, "", ""))

        with self.assertRaises(Exception):
            db.save_marker("test", 1, "", "")
            db.save_marker(1, "test", "", "")
            db.save_marker("test", "test", "", "")

if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    unittest.main()
