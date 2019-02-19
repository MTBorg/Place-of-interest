import psycopg2
from psycopg2.extensions import AsIs

def create_database(existing_db_name, existing_db_superuser_name, existing_db_superuser_pass, host_name, host_port, new_db_name, db_owner):
    """Creates a PostgreSQL database

    This script uses (and requires) the default postgres super user and its password.

    Parameters
    ----------
    existing_db_name: Database name of an existing database.
    existing_db_superuser_name = A existing superuser that has the power to careate a new database.
    existing_db_superuser_pass: Password of the default PostgreSQL user existing_db_superuser_name.
    host_name: Name/address of database host.
    host_port: Port of the host that the database listens to. 
    new_db_name: Name of the database to be created.
    db_owner: Name of the PostgreSQL user to be assigned ownership of the database.
    """
    try:
        connection = psycopg2.connect(
            dbname = existing_db_name, 
            user = existing_db_superuser_name, 
            password = existing_db_superuser_pass,
            host = host_name, 
            port = host_port) 
        connection.autocommit = True #Don't start a transaction (database cannot be created in a transaction)
        cursor = connection.cursor()
        query = "CREATE DATABASE %s OWNER %s;"
        params = (AsIs(new_db_name), db_owner)
        cursor.execute(query, params)

        add_postgis_extension(existing_db_superuser_name, existing_db_superuser_pass, host_name, host_port, new_db_name)
    except Exception as e:
        print("Exception creating database:", e)



def add_postgis_extension(existing_db_superuser_name, existing_db_superuser_pass, host_name, host_port, new_db_name):

    """Creates a Postgis exstension for database

    Parameters
    ----------
    existing_db_superuser_name = A existing superuser that has the power to careate a new database.
    existing_db_superuser_pass: Password of the database user.
    host_name: Name/address of database host.
    host_port: Port of the host that the database listens to. 
    new_db_name: Name of the database that exstenstion is created for.
    """
    try:
        connection = psycopg2.connect(
            dbname = new_db_name, 
            user = existing_db_superuser_name, 
            password = existing_db_superuser_pass, 
            host = host_name, 
            port = host_port)

        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION postgis;")
    except Exception as e:
        print("Exception creating database:", e)

