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

    rw_db_connection = filedata["db_connection"]        # Basic setup connection.
    rw_user = filedata["db_user"]                       # User for read write access.
    rw_db_setup = filedata["db_setup"]                  # Data on existing db and superuser.
    try:
        createDBUser.create_dbuser(rw_db_setup["existing_db_name"],
                                        rw_db_setup["existing_db_superuser_name"],
                                        rw_db_setup["existing_db_superuser_password"],
                                        rw_db_connection["host"],
                                        rw_db_connection["port"],
                                        rw_user["username"],
                                        rw_user["password"])
        
        createDatabase.create_database(rw_db_setup["existing_db_name"],
                                        rw_db_setup["existing_db_superuser_name"],
                                        rw_db_setup["existing_db_superuser_password"],
                                        rw_db_connection["host"],
                                        rw_db_connection["port"],
                                        rw_db_connection["db_name"],
                                        rw_user["username"])
        
        createTables.create_tables(rw_db_setup["existing_db_superuser_name"],
                                        rw_db_setup["existing_db_superuser_password"], 
                                        rw_db_connection["host"], 
                                        rw_db_connection["port"],
                                        rw_db_connection["db_name"])

        grantDBUser.grant_dbuser(rw_db_setup["existing_db_superuser_name"],
                                        rw_db_setup["existing_db_superuser_password"],
                                        rw_db_connection["host"],
                                        rw_db_connection["port"],
                                        rw_db_connection["db_name"],
                                        rw_user["username"])
        
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