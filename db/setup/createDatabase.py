import psycopg2
from psycopg2.extensions import AsIs

def createDatabase(hostName, hostPort, psqlPass, dbName, dbOwner):
    """Creates a PostgreSQL database

    This script uses (and requires) the default postgres super user and its password.

    Parameters
    ----------
    hostName: Name/address of database host
    hostPort: Port of the host that the database listens to 
    psqlPass: Password of the default PostgreSQL user (postgres)
    dbName: Name of the database to be created
    dbOwner: Name of the PostgreSQL user to be assigned ownership of the database
    """
    try:
        connection = psycopg2.connect(
            dbname='postgres', 
            user='postgres', 
            host=hostName, 
            port=hostPort, 
            password=psqlPass) 
        connection.autocommit=True #Don't start a transaction (database cannot be created in a transaction)
        cursor = connection.cursor()
        query = "CREATE DATABASE %s OWNER %s;"
        params = (AsIs(dbName), dbOwner)
        cursor.execute(query, params)
        cursor.execute("CREATE EXTENSION postgis;")
    except Exception as e:
        print("Exception creating database:", e)
