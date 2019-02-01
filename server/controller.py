import sys, bcrypt

sys.path.insert(0,"../db")
import db
#import db.setup.runSetupFiles as setup
#import api.api as api

namn = b"randomstring"
test = bcrypt.hashpw(namn, bcrypt.gensalt())
if(bcrypt.checkpw(namn, test)):
    print("stämmer")
print(test)


class Controller:

    DEFAULT_RADIUS = 1000 #meter?
    db = None

    def __init__(self):
        #create database connection instance to use for db calls.
        self.db = db

    def getMarkersAroundLocation(self, lat, lng):
        '''Retrieves all markers within a given circle from database

        Parameters
        ----------
        lat - latitude
        lng - longitude

        Returns
        -------
        A list containing all markers within the given circle 
        '''
        pass

    def saveMarker(lat, lng, ip, cookieSession):
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
        print("this should save a Marker")

    def initalizeDatabase(self):
        '''Initalizes the databse with all the scripts in setup
        '''
        setup.run()