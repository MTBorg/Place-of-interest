import psycopg2
from psycopg2.extensions import AsIs

def create_database(hostName, hostPort, psqlPass, dbName, dbOwner):
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
        #cursor.execute("CREATE EXTENSION postgis;")
        add_postgis_extension(dbName, dbOwner, hostName, psqlPass, hostPort)
    except Exception as e:
        print("Exception creating database:", e)


def add_postgis_extension(dbname, username, hostname, password, portnr):
    """Creates a Postgis exstension for database

    Parameters
    ----------
    dbname: Name of the database that exstenstion is created for
    username: Name of the PostgreSQL user assigned ownership of the database
    hostname: Name/address of database host
    password: Password of the database user
    postnr: Port of the host that the database listens to 
    """
    try:
        connection = psycopg2.connect(
            dbname=dbname, 
            user=username, 
            host=hostname, 
            password=password, 
            port=portnr)
        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION postgis;")
    except Exception as e:
        print("Exception creating database:", e)

