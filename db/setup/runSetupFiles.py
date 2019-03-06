"""
Runs the all the setup scripts

Arguments
---------
--logLevel: The logging level to use. All logs with a lower level will be ignored.
            Possible options are (from high to low): NONE, CRITICAL, ERROR, WARNING, INFO, DEBUG.
            Default value is INFO. Setting it to NONE will disable logging.
            Refer to https://docs.python.org/3/library/logging.html#logging-levels for more information.
--logFile : The filename of the log file to be produced. Make sure to make it a .log file or git will not ignore it.
            If no filename is specified no log file will be produced.
"""
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
        
        logging.info("Successfully ran setup scripts")

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
    dirname = os.path.dirname(__file__)
    if (dirname == ""): #If the script is run from the same folder we don't want to prepend "/" (as it would result in searching the root)
        filepath = filename
    else:
        filepath = dirname + "/" + filename
    logging.info("Reading file %s", filepath)
    with open(filepath) as f:
        filedata = json.load(f)
    return filedata 

def run():
    """Runs the script and it's functions
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["logLevel=", "logFile="])
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

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
                elif arg == "NONE":
                    logging.info("Disabling logging")
                    logging.disable(logging.CRITICAL)
                else:
                    raise ValueError("Invalid logLevel argument " + arg)
            elif opt=="--logFile":
                flog_handler = logging.FileHandler(arg)
                flog_handler.setLevel(logging.INFO)
                flog_format = logging.Formatter("%(asctime)s %(filename)s %(lineno)s %(funcName)s, %(levelname)s: %(message)s")
                flog_handler.setFormatter(flog_format)
                logging.getLogger().addHandler(flog_handler)

        filename = 'data.json'

        filedata = __load_json_file(filename)
        __run_setup_files(filedata)
    except getopt.GetoptError:
        print("Usage:", os.path.basename(__file__), "--logLevel <logLevel> --logFile <logFile>")
    except OSError:
        logging.exception("OSError")
    except ValueError as e:
        logging.error("ValueError: %s", e)
    except:
        logging.exception("Unknown exception")

if __name__ == "__main__":
    run()
