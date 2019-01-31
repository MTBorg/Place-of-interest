import psycopg2

import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.path.join(ROOT_DIR, 'db/setup')
import setup.runSetupFiles as setup

import json

class db():

    def __init__(self):
        '''Setup a database object based on json-file
        '''
        filename = 'data.json'
        filedata = setup.loadJasonFile(filename)

        db_data = filedata["connection"]
        user_data = filedata["user"]

        self.dbname = db_data["dbname"]
        self.hostname = db_data["host"]
        self.portnr = db_data["port"]
        self.username = user_data["username"]
        self.password = user_data["password"]


    def connect(self):
        ''' Try to connect to database

        Returns
        -------
        Connection to database if no exception
        '''
        try:
            connection = psycopg2.connect(dbname=self.dbname, host=self.hostname, port=self.portnr, user=self.username, password=self.password)
            connection.autocommit=True
            return connection.cursor()
        except Exception as e:
            print("Failed to connect to database:", e)