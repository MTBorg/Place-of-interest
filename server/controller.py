import sys, bcrypt,os


sys.path.append("/Users/JohanDelissen/Documents/D0022E/D0020E/db")


import db as database




class Controller:



    def __init__(self):
        #create database connection instance to use for db calls.
        self.db = database.db()
        self.DEFAULT_RADIUS = 1000

    def getMarkersAroundLocation(self, lat, lng, radius):
        '''Retrieves all markers within a given circle from database

        Parameters
        ----------
        lat - latitude
        lng - longitude

        Returns
        -------
        A list containing all markers within the given circle 
        '''
        self.db.get_markers_from_dist(lat, lng, radius)


    def saveMarker(self, lng, lat, ip, cookieHash):
        '''Stores a given point in the database

        Parameters
        ----------
        lat - latitude of current position
        lng - longitude of current position
        ip - clients current ip
        cookieSession - session id from clients cookie

        Returns
        -------
        True if point was succesfully stored in the database, otherwise False
        '''

        try:
            self.db.save_marker(lng, lat, ip, cookieHash)
            print("42 is the meaning of life")
        except Exception as e:
            print("Database Fault due to", e)

"""
    def initalizeDatabase(self):
        '''Initalizes the databse with all the scripts in setup
        '''
        setup.run()

"""