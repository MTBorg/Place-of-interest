import psycopg2

import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.path.join(ROOT_DIR, 'db/setup')
import setup.runSetupFiles as setup

import json

class db:

    def __init__(self):
        '''Setup a database object based on json-file
        '''
        filename = 'data.json'
        filedata = setup.load_json_file(filename)

        db_data = filedata["connection"]
        user_data = filedata["user"]

        self.dbname = db_data["dbname"]
        self.hostname = db_data["host"]
        self.portnr = db_data["port"]
        self.username = user_data["username"]
        self.password = user_data["password"]


    def __connect(self):
        ''' Try to connect to database

        Returns
        -------
        Connection to database if no exception
        '''
        try:
            connection = psycopg2.connect(dbname=self.dbname, host=self.hostname, port=self.portnr, user=self.username, password=self.password)
            connection.autocommit=True
            return connection
        except Exception as e:
            print("Failed to connect to database:", e)

    def get_markers_from_userid(self, user_id):
        '''Retrieves all markers associated with a given user id

        Parameters
        ----------
        user_id - The id of the user

        Returns
        -------
        A list of tuples of form (longtiude, latitude) associated with the user
        '''
        connection = self.__connect()
        cursor = connection.cursor()

        query = "SELECT ST_X(ST_AsEWKT(marker)), ST_Y(ST_AsEWKT(marker)) FROM markers WHERE user_id=%s;"

        cursor.execute(query, user_id)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_markers_from_dist(self, lng, lat, radius):
        '''Retrieves all markers within a given circle

        Parameters
        ----------
        connection - Cursor for open connection
        lng - Longitude of point in the center of the circle
        lat - Latitude of point in the center of the circle
        radius - The radius of the circle

        Returns
        -------
        A list containing all markers within the given circle 
        '''
        connection = self.__connect()
        cursor = connection.cursor()

        coordinates = "POINT(%s %s)" % (lng, lat)

        query = "SELECT ST_X(ST_AsEWKT(marker)), ST_Y(ST_AsEWKT(marker)) FROM MARKERS WHERE ST_DWithin(%s, marker, %s)"
        data = (coordinates, radius)

        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        return result
        

    def get_markers_from_dist_time(self, lng, lat, radius, startTime, endTime):
        '''Retrieves all markers within a given circle and within a given time interval

        Parameters
        ----------
        lng - Longitude of point in the center of the circle
        lat - Latitude of point in the center of the circle
        radius - The radius of the circle
        startTime - The start of the time interval
        endTime - The end of the time interval

        Returns
        -------
        A list containing all markers within the given circle and time interval
        '''
        connection = self.__connect()
        cursor = connection.cursor()

        coordinates = "POINT(%s %s)" % (lng, lat)

        query = "SELECT ST_X(ST_AsEWKT(marker)), ST_Y(ST_AsEWKT(marker)) FROM MARKERS WHERE ST_DWithin(%s, marker, %s) AND %s <= created_at AND %s >= created_at"
        data = (coordinates, radius, startTime, endTime)

        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        return result

    def save_marker(self, lng, lat, user_id):
        '''Stores a given point in the database

        Parameters
        ----------
        connection - Connection to database
        lng - Longitude of marker position
        lat - Latitude of marker position
        user_id - The id of the user

        Returns
        -------
        True if point was succesfully stored in the database, otherwise False
        '''
        connection = self.__connect()
        cursor = connection.cursor()

        coordinates = "POINT(%s %s)" % (lng, lat)
        query = "INSERT INTO markers (marker, user_id) VALUES (ST_GeomFromText(%s, 4326), %s)"
        data = (coordinates, user_id)

        cursor.execute(query, data)
        cursor.close()