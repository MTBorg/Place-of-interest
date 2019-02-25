import unittest
import db as database
import logging
import json
import psycopg2
from psycopg2.extensions import AsIs

from setup import createDatabase, createDBUser, createTables, grantDBUser

class dbTest(unittest.TestCase):
    def setUp(self):
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
                points = [
                    {"marker": (0,0), "ip_address": "123.123.123.123", "user_id": 0},
                    {"marker": (100,100), "ip_address": "192.168.10.34", "user_id": 1},
                    {"marker": (-10,0), "ip_address": "123.123.123.123", "user_id": 2}
                ]
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
    
    def test_get_markers_from_ip(self):
        logging.info("Testing getting markers from ip")
    
    def test_get_markers_from_userid_and_ip(self):
        logging.info("Testing getting markers from user id and ip")
    
    def test_get_markers_from_dist(self):
        logging.info("Testing getting markers from distance")

    def test_get_markers_from_dist_time(self):
        logging.info("Testing getting markers from distance and time")

    def test_save_marker(self):
        logging.info("Testing saving marker")


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    unittest.main()
