import unittest
import sanitize as s
import logging
import json
import psycopg2
import datetime
from psycopg2.extensions import AsIs

class sanitizeTest(unittest.TestCase):

    def test_cookieCheck(self):
        logging.info("Test cookieCheck")
        sanitizer = s.Sanitizer()
        #request = ""
        #self.assertTrue(sanitizer.cookieCheck(request))


    def test_getHashCookie(self):
        logging.info("Test getHashCookie")
        sanitizer = s.Sanitizer()
        #result = ""
        #self.assertIn(sanitizer.getHashCookie(), result)


    def test_checkHashCookie(self):
        logging.info("Test checkHashCookie")
        sanitizer = s.Sanitizer()
        cookieHash = "$2b$12$swUd.H2yI1GFO05h/946o.v8qJS4eQE8y0fMxtou2Nr433wAGWQDW"
        self.assertTrue(sanitizer.checkHashCookie(cookieHash))

        cookieHash = "$2b$12$swUd.H2yI1GFO05h/946o.v8qJS4eQE8t0fMxtou2Nr433wAGWQDW"
        self.assertFalse(sanitizer.checkHashCookie(cookieHash))


    def test_checkTimeCookie(self):
        logging.info("Test checkTimeCookie")
        sanitizer = s.Sanitizer()
        #cookieTime = datetime.datetime(2019, 1, 31, 0, 0, 0, 0)
        #self.assertTrue(sanitizer.checkHashCookie(cookieTime))


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    unittest.main()
