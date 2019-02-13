import psycopg2
from psycopg2.extensions import AsIs
import logging

def grant_dbuser(db_name, dbuser_name, host_name, host_port, psql_pass):
    '''Connects to the specified database and gives the specified
    user grants to the markers table

    Parameters
    ----------
    db_name: The name of the database in which the markers table is present
    dbuser_name: The name of the user to be given the grants
    host_name: The name of the database host
    host_port: The port of the database
    psql_pass: The password to the default postgres user
    '''
    try:
        logging.info("Connecting to database %s as user postgres on host %s port %s", db_name, host_name, host_port) 
        connection = psycopg2.connect(
            dbname = db_name,
            user = 'postgres',
            host = host_name,
            port = host_port,
            password = psql_pass,
        )
        connection.autocommit = True
        cursor = connection.cursor()

        logging.info("Granting SELECT, INSERT and DELETE to user %s", dbuser_name)
        query = '''
            GRANT
            SELECT, INSERT, DELETE
            ON markers
            TO %s;'''
        params = (AsIs(dbuser_name),)
        cursor.execute(query, params)

        #Grant the user the USAGE privilege on the marker id sequence (SERIAL)
        logging.info("Granting USAGE on id sequence to user %s", dbuser_name)
        query = '''
            GRANT
            USAGE
            ON markers_id_seq
            TO %s;'''
        params = (AsIs(dbuser_name),)
        cursor.execute(query, params)

        logging.info("Successfully granted user %s", dbuser_name)
    except Exception as e:
        print("Error giving user grants", e)