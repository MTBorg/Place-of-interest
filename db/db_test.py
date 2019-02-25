import unittest
import db
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
                test_user = conf["test_user"]
                superuser = conf["superuser"]
                database = conf["database"]
                psql_connection = conf["psql_connection"]

                # Connect to the default database
                db_connection = psycopg2.connect(
                    dbname="postgres",
                    user=superuser["name"],
                    password = superuser["password"],
                    host = psql_connection["host"],
                    port = psql_connection["port"]
                )
                db_connection.autocommit = True
                db_cursor = db_connection.cursor()

                # Drop the database
                logging.info("Dropping database %s in preparation for test", database["name"])
                try:
                    db_cursor.execute("DROP DATABASE %s;", (AsIs(database["name"]),))
                except psycopg2.Error as e:
                    if (e.pgcode == '3D000'): # invalid_catalog_name error code
                        logging.info("Could not find database %s, continuing...", database["name"])
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
                    host_name=psql_connection["host"],
                    host_port=psql_connection["port"],
                    psql_pass= superuser["password"],
                    dbuser_name = test_user["name"],
                    dbuser_pass = test_user["password"]
                )

                #Create database
                logging.info("Setting up test database %s", database["name"])
                createDatabase.create_database(
                    host_name=psql_connection["host"],
                    host_port=psql_connection["port"],
                    psql_pass=superuser["password"],
                    db_name = database["name"],
                    db_owner = superuser["name"]
                )

                #Create tables
                logging.info("Setting up tables")
                createTables.create_tables(
                    dbname = database["name"],
                    username = superuser["name"],
                    hostname = psql_connection["host"],
                    password = superuser["password"],
                    portnr = psql_connection["port"]
                )

                # Give database user grants
                logging.info("Giving user %s grants", test_user["name"])
                grantDBUser.grant_dbuser(
                    db_name = database["name"],
                    dbuser_name = test_user["name"],
                    host_name = psql_connection["host"],
                    host_port = psql_connection["port"],
                    psql_pass = superuser["password"]
                )
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