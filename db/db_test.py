import unittest
import db as database
import logging
import json
import psycopg2
from psycopg2.extensions import AsIs

from setup import createDatabase, createDBUser, createTables, grantDBUser

class dbTest(unittest.TestCase):
    def setUp(self):
        # WARNING: DO NOT remove or edit points (unless you really know what you are doing) as this will most likely break already implemented tests.
        # Instead just add new ones.
        points = [
            {"marker": (0,0), "ip_address": "123.123.123.123", "user_id": "0"},
            {"marker": (100,80), "ip_address": "192.168.10.34", "user_id": "1"},
            {"marker": (-10,0), "ip_address": "123.123.123.123", "user_id": "2"},
            {"marker": (65.58544844,22.1511663), "ip_address": "234.234.234.234", "user_id": "3"}, # Kulturens hus, Luleå
            {"marker": (65.6181932,22.1339231), "ip_address": "234.234.234.234", "user_id": "3"} # Aula Aurora, Luleå University of Technology, Luleå
        ]
        try:
            logging.info("Reading configuration file test_conf.json")
            with open('testConf.json') as f:
                conf = json.load(f)
                test_user = conf["poi_user"]
                test_db = conf["poi_db"]
                superuser = conf["superuser"]
                connection = conf["connection"]

                # Connect to the default database
                db_connection = psycopg2.connect(
                    dbname = "postgres",
                    user = superuser["name"],
                    password = superuser["password"],
                    host = connection["host"],
                    port = connection["port"]
                )
                db_connection.autocommit = True
                db_cursor = db_connection.cursor()

                # Drop the database
                logging.info("Dropping database %s in preparation for test", test_db["name"])
                try:
                    db_cursor.execute("DROP DATABASE %s;", (AsIs(test_db["name"]),))
                except psycopg2.Error as e:
                    if (e.pgcode == '3D000'): # invalid_catalog_name error code
                        logging.info("Could not find database %s, continuing...", test_db["name"])
                    else:
                        raise
                
                # Drop the user
                logging.info("Dropping user %s in preparation for test", test_user["name"])
                try:    
                    db_cursor.execute("DROP ROLE %s;", (AsIs(test_user["name"]),))
                except psycopg2.ProgrammingError as e:
                    if (e.pgcode == '42704'): # undefined_object error code
                        logging.info("Could not find user %s, continuing...", test_user["name"])
                    else:
                        raise

                #Create database user
                logging.info("Setting up test user %s", test_user["name"])
                createDBUser.create_dbuser(
                    host_name = connection["host"],
                    host_port = connection["port"],
                    psql_pass = superuser["password"],
                    dbuser_name = test_user["name"],
                    dbuser_pass = test_user["password"]
                )

                #Create database
                logging.info("Setting up test database %s", test_db["name"])
                createDatabase.create_database(
                    host_name=connection["host"],
                    host_port=connection["port"],
                    psql_pass=superuser["password"],
                    db_name = test_db["name"],
                    db_owner = superuser["name"]
                )

                #Create tables
                logging.info("Setting up tables")
                createTables.create_tables(
                    dbname = test_db["name"],
                    username = superuser["name"],
                    hostname = connection["host"],
                    password = superuser["password"],
                    portnr = connection["port"]
                )

                # Give the database user grants
                logging.info("Giving user %s grants", test_user["name"])
                grantDBUser.grant_dbuser(
                    db_name = test_db["name"],
                    dbuser_name = test_user["name"],
                    host_name = connection["host"],
                    host_port = connection["port"],
                    psql_pass = superuser["password"]
                )

                #Insert test points
                logging.info("Connecting to database %s to insert points", test_db["name"])
                db = database.db("../testConf.json") # NOTE: The path is relative to the db file
                logging.info("Inserting %s points", len(points))
                for point in points:
                    db.save_marker(
                        lng = point["marker"][0],
                        lat = point["marker"][1],
                        ip_address = point["ip_address"],
                        user_id = point["user_id"]
                    )
                logging.info("Test database %s was successfully setup", test_db["name"])
        except:
            logging.exception("Unknown exception")

    def test_get_markers_from_userid(self):
        logging.info("Testing getting markers from user id")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        self.assertIn((0.0,0.0), db.get_markers_from_userid("0"))
        self.assertIn((100, 80), db.get_markers_from_userid("1"))
        self.assertIn((-10,0), db.get_markers_from_userid("2"))
        self.assertNotIn((100, 80), db.get_markers_from_userid("0"))
        self.assertEqual(len(db.get_markers_from_userid("454312")), 0)

        self.assertEqual(db.get_markers_from_userid("0"), [(0,0)])
        self.assertEqual(db.get_markers_from_userid("1"), [(100,80)])
        self.assertEqual(db.get_markers_from_userid("2"), [(-10,0)])
        self.assertEqual(db.get_markers_from_userid("66"), [])
        self.assertFalse(db.get_markers_from_userid("1") == [(80,100)])
        self.assertFalse(db.get_markers_from_userid("2") == [(10,0)])
        self.assertFalse(db.get_markers_from_userid("0") == [(0.001,0.001)])
        self.assertFalse(db.get_markers_from_userid("66") == [(0.001,0.001)])    

    def test_get_markers_from_ip(self):
        logging.info("Testing getting markers from ip")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        self.assertIn((0,0), db.get_markers_from_ip("123.123.123.123"))
        self.assertIn((-10,0), db.get_markers_from_ip("123.123.123.123"))
        self.assertIn((100,80), db.get_markers_from_ip("192.168.10.34"))
        self.assertNotIn((0,0), db.get_markers_from_ip("192.168.10.34"))

        self.assertEqual(db.get_markers_from_ip("123.123.123.123"), [(-10,0),(0,0)])
        self.assertEqual(db.get_markers_from_ip("192.168.10.34"), [(100,80)])
        self.assertEqual(db.get_markers_from_ip("77"), [])
        self.assertFalse(db.get_markers_from_ip("192.168.10.34") == [(80,100)])
        self.assertFalse(db.get_markers_from_ip("192.168.10.34") == [(100.0001,80.001)])
        self.assertFalse(db.get_markers_from_ip("77") == [(100.0001,80.001)])
    
    def test_get_markers_from_userid_and_ip(self):
        logging.info("Testing getting markers from user id and ip")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file
        self.assertEqual(db.get_markers_from_userid_and_ip("0", "123.123.123.123"), [(0,0)])
        self.assertEqual(db.get_markers_from_userid_and_ip("1", "192.168.10.34"), [(100,80)])
        self.assertEqual(db.get_markers_from_userid_and_ip("2", "123.123.123.123"), [(-10,0)])
        self.assertEqual(db.get_markers_from_userid_and_ip("66","77"), [])
        self.assertFalse(db.get_markers_from_userid_and_ip("1", "192.168.10.34") == [(80,100)])
        self.assertFalse(db.get_markers_from_userid_and_ip("2", "123.123.123.123") == [(10,0)])
        self.assertFalse(db.get_markers_from_userid_and_ip("66", "77") == [(10,0)])
    
    def test_get_markers_from_dist(self):
        logging.info("Testing getting markers from distance")
        db = database.db("../testConf.json") # NOTE: The path is relative to the db file

        # Tests between kulturens hus, Luleå and the roundabout outside
        self.assertIn((65.58544844,22.1511663), db.get_markers_from_dist(65.5856349,22.1509888, 200))
        self.assertNotIn((65.58544844,22.1511663), db.get_markers_from_dist(65.5856349,22.1509888, 10))

        # Tests between Aula Aurora, Luleå and Luleå train station, distance: ~4.7km
        self.assertIn((65.6181932,22.1339231), db.get_markers_from_dist(65.5839882,22.1627801, 4800)) # NOTE: Maybe give some more margin for error
        self.assertNotIn((65.6181932,22.1339231), db.get_markers_from_dist(65.5856349,22.1627801, 4600))

    def test_get_markers_from_dist_time(self):
        logging.info("Testing getting markers from distance and time")

    def test_save_marker(self):
        logging.info("Testing saving marker")
        db = database.db("../testConf.json")

        #testing valid input format
        self.assertTrue(db.save_marker(0.0, 0.0, "ip_address", "user_id"))
        self.assertTrue(db.save_marker("0.0", 0.0, "ip_address", "user_id"))
        self.assertTrue(db.save_marker(0.0, "0.0", "ip_address", "user_id"))
        self.assertTrue(db.save_marker(0.0, 0.0, 0, "user_id"))
        self.assertTrue(db.save_marker(0.0, 0.0, "ip_address", 0))
        self.assertTrue(db.save_marker(0.0, 0.0, 11, "user_id"))
        self.assertTrue(db.save_marker(0.0, 0.0, "ip_address", 11))

        #testing random values for lng and lat
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
