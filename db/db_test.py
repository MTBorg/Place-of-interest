import unittest
import db
import logging
from setup import createDatabase, createDBUser, createTables

class dbTest(unittest.TestCase):
    def setUp(self):
        logging.info("Setting up test database")

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