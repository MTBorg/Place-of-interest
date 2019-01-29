import createDatabase
import createDBUser
import createTables
import json


def __runSetupFiles(filedata):    
    """Runs the three setup scripts and feeds them data from the variable filedata

    Parameters
    ----------
    filedata: Is a dictionary with all the json data containing the keys connect and users
    """
    connection_dict = filedata["connection"]    # basic setup connection
    rw_user = filedata["user"]                  # user for read write access
    try:
        createDBUser.createDBUser(connection_dict["host"], connection_dict["port"], 
                rw_user["password"], connection_dict["password"], rw_user["username"])
        
        createDatabase.createDatabase(connection_dict["host"], 
                connection_dict["port"], connection_dict["password"], 
                connection_dict["dbname"], connection_dict["user"])
        
        createTables.createTables(connection_dict["dbname"], connection_dict["user"], 
                connection_dict["host"], connection_dict["password"], connection_dict["port"])

    except Exception as e:
        print("Error 1, Exception:", e)

def loadJasonFile(filename):
    """Loads file and returns all the data

    Parameters
    ----------
    filename: Name of the json file that will be loaded
    
    Returns
    ----------
    A dictionary with all the data from the json file
    """
    try:
        with open(filename) as f:
            filedata = json.load(f)
    except Exception as e:
        print("Error 2, Exception:", e)
        return
    return filedata 

def run():
    """Runs the script and it's functions
    """
    filename = 'data.json'
    filedata = loadJasonFile(filename)
    __runSetupFiles(filedata)


#test script
#run()