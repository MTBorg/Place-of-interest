import createDatabase
import createDBUser
import createTables
import grantDBUser

import logging
import json
import os
import sys
import getopt

def __run_setup_files(filedata):    

    """Runs the three setup scripts and feeds them data from the variable filedata

    Parameters
    ----------
    filedata: Is a dictionary with all the json data containing the keys connect and users
    """

    connection_dict = filedata["connection"]    # basic setup connection
    rw_user = filedata["user"]                  # user for read write access
    try:
        createDBUser.create_dbuser(connection_dict["host"], connection_dict["port"], 
                connection_dict["password"], rw_user["username"], rw_user["password"])
        
        createDatabase.create_database(connection_dict["host"], 
                connection_dict["port"], connection_dict["password"], 
                connection_dict["dbname"], rw_user["username"])
        
        createTables.create_tables(connection_dict["dbname"], connection_dict["user"], 
                connection_dict["host"], connection_dict["password"], connection_dict["port"])

        grantDBUser.grant_dbuser(connection_dict["dbname"], rw_user["username"],
                connection_dict["host"], connection_dict["port"], connection_dict["password"])
        
    except Exception as e:
        print("Exception while running setup scripts:", e)


def load_json_file(filename):

    """Loads file and returns all the data

    Parameters
    ----------
    filename: Name of the json file that will be loaded
    
    Returns
    ----------
    A dictionary with all the data from the json file
    """
    try:
        filepath = os.path.dirname(__file__) + "/" + filename
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

    filedata = load_json_file(filename)
    __run_setup_files(filedata)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        opts, args = getopt.getopt(sys.argv[1:], "", ["logLevel="])

        #Parse command line arguments
        for opt, arg in opts:
            if opt=="--logLevel":
                if arg == "CRITICAL":
                    logging.info("Setting log level to critical")
                    logging.basicConfig(level=logging.CRITICAL)
                elif arg == "ERROR":
                    logging.info("Setting log level to error")
                    logging.basicConfig(level=logging.ERROR)
                elif arg == "WARNING":
                    logging.info("Setting log level to warning")
                    logging.basicConfig(level=logging.WARNING)
                elif arg == "INFO":
                    logging.info("Setting log level to info")
                    logging.basicConfig(level=logging.INFO)
                elif arg == "DEBUG":
                    logging.info("Setting log level to debug")
                    logging.basicConfig(level=logging.DEBUG)
                else:
                    raise Exception("Invalid logLevel argument " + arg)
        
        run()
    except getopt.GetoptError:
        print("Usage:", os.path.basename(__file__), "--logLevel <logLevel>")
    except Exception as e:
        print("Exception:", e)