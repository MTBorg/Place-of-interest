import psycopg2
from psycopg2.extensions import AsIs

import logging

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
        logging.info("Connecting to database postgres as user postgres on host %s port %s", db_host, db_port) 
        connection = psycopg2.connect(
            dbname = default_db_name, 
            user = superuser_name, 
            password = superuser_password,
            host = db_host, 
            port = db_port) 
        connection.autocommit = True #Don't start a transaction (database cannot be created in a transaction)
        cursor = connection.cursor()

        logging.info("Creating database %s with owner %s", poi_db_name, db_owner)
        query = "CREATE DATABASE %s OWNER %s;"
        params = (AsIs(poi_db_name), db_owner)
        cursor.execute(query, params)
        logging.info("Successfully created database %s with owner %s", poi_db_name, db_owner)

        add_postgis_extension(superuser_name, superuser_password, db_host, db_port, poi_db_name)
    except psycopg2.Error as e:
        if e.pgcode == '42P04': #duplicate_database code
            logging.warning("Database %s already exists. Make sure it has the correct tables and postgis enabled or delete it and run the setup script again", poi_db_name)
        else:
            raise Exception("Exception creating database " + poi_db_name + ": " + str(e))
    except Exception as e:
        raise Exception("Exception creating database " + poi_db_name + ": " + str(e))



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
        logging.info("Connecting to database %s as user postgres on host %s port %s", poi_db_name, db_host, db_port) 
        connection = psycopg2.connect(
            dbname = poi_db_name, 
            user = superuser_name, 
            password = superuser_password, 
            host = db_host, 
            port = db_port)

        connection.autocommit=True
        cursor = connection.cursor()

        logging.info("Enabling extension postgis for database %s", poi_db_name)
        cursor.execute("CREATE EXTENSION postgis;")
        logging.info("Successfully enabled postgis for database %s", poi_db_name)
    except Exception as e:
        print("Exception creating database:", e)

