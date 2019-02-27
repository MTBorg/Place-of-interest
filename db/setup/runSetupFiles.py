import createDatabase
import createDBUser
import createTables
import grantDBUser

import json
import os
from pathlib import Path

def __run_setup_files(filedata):    

    """Runs the three setup scripts and feeds them data from the variable filedata

    Parameters
    ----------
    filedata: Is a dictionary with all the json data containing the keys connect and users
    """

    connection = filedata["connection"]     # Basic setup connection.
    poi_user = filedata["poi_user"]         # User for read write access.
    poi_db = filedata["poi_db"]
    superuser = filedata["superuser"]
    default_db = filedata["default_db"]
    try:
        createDBUser.create_dbuser(default_db["name"],
                                        superuser["name"],
                                        superuser["password"],
                                        connection["host"],
                                        connection["port"],
                                        poi_user["name"],
                                        poi_user["password"])
        
        createDatabase.create_database(default_db["name"],
                                        superuser["name"],
                                        superuser["password"],
                                        connection["host"],
                                        connection["port"],
                                        poi_db["name"],
                                        poi_user["name"])
        
        createTables.create_tables(superuser["name"],
                                        superuser["password"],
                                        connection["host"],
                                        connection["port"],
                                        poi_db["name"])

        grantDBUser.grant_dbuser(superuser["name"],
                                        superuser["password"],
                                        connection["host"],
                                        connection["port"],
                                        poi_db["name"],
                                        poi_user["name"])
        
    except Exception as e:
        print("Exception while running setup scripts:", e)


def __load_json_file(filename):

    """Loads file and returns all the data

    Parameters
    ----------
    filename: Name of the json file that will be loaded
    
    Returns
    ----------
    A dictionary with all the data from the json file
    """
    try:
        dirname = os.path.dirname(__file__)
        if (dirname == ""): #If the script is run from the same folder we don't want to prepend "/" (as it would result in searching the root)
            filepath = filename
        else:
            filepath = dirname + "/" + filename
        with open(filepath) as f:
            filedata = json.load(f)
    except Exception as e:
        print("Exception while loading JSON file:", e)
        return
    return filedata 

def run():
    """Runs the script and it's functions
    """
    filename = 'data.json'

    filedata = __load_json_file(filename)
    __run_setup_files(filedata)

if __name__ == "__main__":
    run()