import psycopg2
from psycopg2.extensions import AsIs

def create_database(default_db_name, superuser_name, superuser_password, db_host, db_port, poi_db_name, db_owner):
    """Creates a PostgreSQL database

    This script uses (and requires) the default postgres super user and its password.

    Parameters
    ----------
    default_db_name: Database name of an existing database.
    superuser_name = A existing superuser that has the power to careate a new database.
    superuser_password: Password of the default PostgreSQL user superuser_name.
    db_host: Name/address of database host.
    db_port: Port of the host that the database listens to. 
    poi_db_name: Name of the database to be created.
    db_owner: Name of the PostgreSQL user to be assigned ownership of the database.
    """
    try:
        connection = psycopg2.connect(
            dbname = default_db_name, 
            user = superuser_name, 
            password = superuser_password,
            host = db_host, 
            port = db_port) 
        connection.autocommit = True #Don't start a transaction (database cannot be created in a transaction)
        cursor = connection.cursor()
        query = "CREATE DATABASE %s OWNER %s;"
        params = (AsIs(poi_db_name), db_owner)
        cursor.execute(query, params)

        add_postgis_extension(superuser_name, superuser_password, db_host, db_port, poi_db_name)
    except Exception as e:
        print("Exception creating database:", e)



def add_postgis_extension(superuser_name, superuser_password, db_host, db_port, poi_db_name):

    """Creates a Postgis exstension for database

    Parameters
    ----------
    superuser_name = A existing superuser that has the power to careate a new database.
    superuser_password: Password of the database user.
    db_host: Name/address of database host.
    db_port: Port of the host that the database listens to. 
    poi_db_name: Name of the database that exstenstion is created for.
    """
    try:
        connection = psycopg2.connect(
            dbname = poi_db_name, 
            user = superuser_name, 
            password = superuser_password, 
            host = db_host, 
            port = db_port)

        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION postgis;")
    except Exception as e:
        print("Exception creating database:", e)

