import createDatabase
import createDBUser
import createTables
import json
import os

def __runSetupFiles(filedata):    
    """Runs the three setup scripts and feeds them data from the variable filedata

    Parameters
    ----------
    filedata: Is a dictionary with all the json data containing the keys connect and users
    """
    connection_dict = filedata["connection"]
    try:
        for user in filedata["users"]:
            createDBUser.createDBUser(connection_dict["host"], connection_dict["port"], 
                    user["password"], 
                    connection_dict["password"], user["username"])
        
        createDatabase.createDatabase(connection_dict["host"], 
                connection_dict["port"], connection_dict["password"], 
                connection_dict["dbname"], connection_dict["user"])
        createTables.createTables(connection_dict["dbname"], connection_dict["user"], 
                connection_dict["host"], connection_dict["password"], connection_dict["port"])
    except Exception as e:
        print("Exception while running setup scripts:", e)

def __loadJsonFile(filename):
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
    filedata = __loadJsonFile(filename)
    __runSetupFiles(filedata)


run()