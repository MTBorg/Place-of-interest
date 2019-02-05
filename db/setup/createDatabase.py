import psycopg2
from psycopg2.extensions import AsIs

def create_database(host_name, host_port, psql_pass, db_name, db_owner):
    """Creates a PostgreSQL database

    This script uses (and requires) the default postgres super user and its password.

    Parameters
    ----------
    host_name: Name/address of database host
    host_port: Port of the host that the database listens to 
    psql_pass: Password of the default PostgreSQL user (postgres)
    db_name: Name of the database to be created
    db_owner: Name of the PostgreSQL user to be assigned ownership of the database
    """
    try:
        connection = psycopg2.connect(
            db_name='postgres', 
            user='postgres', 
            host=host_name, 
            port=host_port, 
            password=psql_pass) 
        connection.autocommit=True #Don't start a transaction (database cannot be created in a transaction)
        cursor = connection.cursor()
        query = "CREATE DATABASE %s OWNER %s;"
        params = (AsIs(db_name), db_owner)
        cursor.execute(query, params)
        add_postgis_extension(db_name, db_owner, host_name, psql_pass, host_port)
    except Exception as e:
        print("Exception creating database:", e)


def add_postgis_extension(db_name, username, host_name, password, portnr):
    """Creates a Postgis exstension for database

    Parameters
    ----------
    db_name: Name of the database that exstenstion is created for
    username: Name of the PostgreSQL user assigned ownership of the database
    host_name: Name/address of database host
    password: Password of the database user
    postnr: Port of the host that the database listens to 
    """
    try:
        connection = psycopg2.connect(
            db_name=db_name, 
            user=username, 
            host=host_name, 
            password=password, 
            port=portnr)
        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION postgis;")
    except Exception as e:
        print("Exception creating database:", e)

