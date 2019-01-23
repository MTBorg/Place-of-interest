import psycopg2
from psycopg2.extensions import AsIs

def createDBUser(hostName, hostPort, psqlPass, dbName, dbOwner):
    """Creates a user for access to database

    Parameters
    ----------
    hostName: Name/address of database host
    hostPort: Port of the host that the database listens to 
    psqlPass: Password of the default PostgreSQL user (postgres)
    dbName: Name of the database to be created
    dbOwner: Name of the PostgreSQL user to be assigned ownership of the database
    """
    try:
        connection = psycopg2.connect(dbname='postgres', user='postgres', host=hostname, password=psqlPass, port=hostPort)
        connection.autocommit=True
        cursor = connection.cursor()
        SQL = "CREATE USER %s WITH ENCRYPTED PASSWORD %s"
        query = "CREATE DATABASE %s OWNER %s;"
        data = (AsIs(dbOwner), psqlPass)
        cursor.execute(SQL, data)
    except Exception as e:
        print("Exception:", e)