import psycopg2
import logging
from psycopg2.extensions import AsIs


def create_dbuser(host_name, host_port, psql_pass, dbuser_name, dbuser_pass):

    """Creates a user for access to database

    Parameters
    ----------
    host_name: Name/address of database host
    host_port: Port of the host that the database listens to 
    psql_pass: Password of the default PostgreSQL user (postgres)
    dbuser_name: The name of the user to create
    dbuser_pass: The password for the new user
    """
    try:
        logging.info("Connecting to database postgres as user postgres at host %s port %s", host_name, host_port)
        connection = psycopg2.connect(dbname='postgres', user='postgres', host=host_name, password=psql_pass, port=host_port)
        connection.autocommit=True
        cursor = connection.cursor()
        logging.info("Creating role %s", dbuser_name)
        query = '''CREATE ROLE %s WITH 
                NOSUPERUSER
                NOCREATEDB
                NOCREATEROLE
                NOINHERIT
                LOGIN
                CONNECTION LIMIT -1
                ENCRYPTED PASSWORD %s'''
        params = (AsIs(dbuser_name), dbuser_pass)
        cursor.execute(query, params)
    except psycopg2.ProgrammingError as e:
        if e.pgcode == '42710': #duplicate_object error code
            logging.warning("Role %s already exists. Make sure it has the necessary privileges or delete it and run the setup script again", dbuser_name)
        else:
            raise Exception("Exception creating user" + dbuser_name + ": " + str(e))
    except Exception as e:
        raise Exception("Exception creating user:" + str(e))

