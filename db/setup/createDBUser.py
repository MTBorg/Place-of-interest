import psycopg2
from psycopg2.extensions import AsIs

def createDBUser(hostName, hostPort, psqlPass, dbPass, dbOwner):
    """Creates a user for access to database

    Parameters
    ----------
    hostName: Name/address of database host
    hostPort: Port of the host that the database listens to 
    psqlPass: Password of the default PostgreSQL user (postgres)
    dbName: Name of the database to be created
    dbPass: Password for database
    dbOwner: Name of the PostgreSQL user to be assigned ownership of the database
    """
    try:
        connection = psycopg2.connect(dbname='postgres', user='postgres', host=hostName, password=dbPass, port=hostPort)
        connection.autocommit=True
        cursor = connection.cursor()
        SQL = "CREATE USER %s WITH ENCRYPTED PASSWORD %s"
        data = (AsIs(dbOwner), psqlPass)
        cursor.execute(SQL, data)
    except Exception as e:
        print("Exception creating user:", e)

def grantDBUserPrivileges(database, hostName, hostPort, dbPass, dbOwner):
    """Granting privileges to a database user 

    Parameters
    ----------
    hostName: Name/address of database host
    hostPort: Port of the host that the database listens to 
    psqlPass: Password of the default PostgreSQL user (postgres)
    dbName: Name of the database to be created
    dbPass: Password for database user
    dbOwner: Name of the PostgreSQL user to be assigned ownership of the database
    """
    try:
        connection = psycopg2.connect(dbname=database, user='postgres', host=hostName, password=dbPass, port=hostPort)
        connection.autocommit=True
        cursor = connection.cursor()
        SQL = "ALTER ROLE admin SUPERUSER NOCREATEDB NOCREATEROLE"
        cursor.execute(SQL)
    except Exception as e:
        print("Exception Granting privileges:", e)