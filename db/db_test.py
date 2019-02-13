import unittest
import db
import logging
import json
import psycopg2

from setup import createDatabase, createDBUser, createTables, clearDB

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

                logging.info("Clearing user %s in preparation for test", test_user["name"])
                try:
                    clearDB.dropUser(
                        host_name = psql_connection["host"],
                        host_port = psql_connection["port"],
                        su_name = superuser["name"],
                        su_pass = superuser["password"],
                        user_name = test_user["name"]
                    )
                except psycopg2.ProgrammingError as e:
                    if (e.pgcode == 42704): # undefined_object error code
                        logging.info("Could not find test user")
                    else:
                        logging.exception("Unknown exception")

                
                logging.info("Clearing database %s in preparation for test", database["name"])
                try:    
                    clearDB.dropDatabase(
                        db_name = database["name"],
                        host_name = psql_connection["host"],
                        host_port = psql_connection["port"],
                        su_name = 'postgres',
                        su_pass = superuser["password"]
                    )
                except psycopg2.ProgrammingError as e:
                    if (e.pgcode == 42704): # undefined_object error cde
                        logging.info("Could no find test database %s", database["name"])
                    else:
                        logging.exception("Unknown exception")

                logging.info("Setting up test database %s", database["name"])

                #Create database user
                createDBUser.create_dbuser(
                    host_name=psql_connection["host"],
                    host_port=psql_connection["port"],
                    psql_pass= superuser["password"],
                    dbuser_name = test_user["name"],
                    dbuser_pass = test_user["password"]
                )

                #Create database
                createDatabase.create_database(
                    host_name=psql_connection["host"],
                    host_port=psql_connection["port"],
                    psql_pass=superuser["password"],
                    db_name = database["name"],
                    db_owner = superuser["name"]
                )

                #Create tables
                createTables.create_tables(
                    dbname = database["name"],
                    username = superuser["name"],
                    hostname = psql_connection["host"],
                    password = superuser["password"],
                    portnr = psql_connection["port"]
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