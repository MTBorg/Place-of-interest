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
    logging.info("Running setup scripts")
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
        logging.info("Successfully ran setup scripts")
    except Exception as e:
        raise e


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
        logging.info("Reading file %s", filepath)
        with open(filepath) as f:
            filedata = json.load(f)
        return filedata 
    except Exception as e:
        #logging.error("Exception while reading file %s: %s", filepath, e)
        raise Exception("Exception while reading file "+ filepath + ": " + str(e))

def run():
    """Runs the script and it's functions
    """
    try:
        filename = 'data.json'

        filedata = load_json_file(filename)
        __run_setup_files(filedata)
    except:
        raise

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["logLevel="])
        logging.basicConfig(format="%(asctime)s, %(levelname)s: %(message)s", level=logging.INFO)

        #Parse command line arguments
        for opt, arg in opts:
            if opt=="--logLevel":
                logger = logging.getLogger()
                if arg == "CRITICAL":
                    logging.info("Setting log level to critical")
                    logger.setLevel(level=logging.CRITICAL)
                elif arg == "ERROR":
                    logging.info("Setting log level to error")
                    logger.setLevel(level=logging.ERROR)
                elif arg == "WARNING":
                    logging.info("Setting log level to warning")
                    logger.setLevel(level=logging.WARNING)
                elif arg == "INFO":
                    logging.info("Setting log level to info")
                    logger.setLevel(level=logging.INFO)
                elif arg == "DEBUG":
                    logging.info("Setting log level to debug")
                    logger.setLevel(level=logging.DEBUG)
                else:
                    raise Exception("Invalid logLevel argument " + arg)
        
        run()
    except getopt.GetoptError:
        print("Usage:", os.path.basename(__file__), "--logLevel <logLevel>")
    except Exception as e:
        logging.error(e)
        raise e