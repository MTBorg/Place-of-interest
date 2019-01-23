import createDatabase
import createDBUser
import createTables
import json


def __runSetupFiles(filedata, connection_dict):
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
        print("Error 1, Exception:", e)

def __loadJasonFile(filename):
    try:
        with open(filename) as f:
            filedata = json.load(f)
    except Exception as e:
        print("Error 2, Exception:", e)
        return
    return filedata 

def __getConnection_dict(filedata):
    if "connection" in filedata:
        print("connection from file")
        return filedata["connection"]
    return {"dbname" : "postgres", "user" : "postgres", 
                "host" : "localhost", "password" : "123", 
                "port" : "5432"}



def run():
    print("test")
    filename = 'data.json'
    filedata = __loadJasonFile(filename)
    conection_dict = __getConnection_dict(filedata)
    __runSetupFiles(filedata, conection_dict)


run()