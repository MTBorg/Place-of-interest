import psycopg2
from psycopg2.extensions import AsIs
import logging

def grant_dbuser(superuser_name, superuser_password, db_host, db_port, poi_db_name, poi_user_name):
    '''Connects to the specified database and gives the specified
    user grants to the markers table

    Parameters
    ----------
    superuser_name = A existing superuser that has the power to careate a new database.
    superuser_password: Password of the default PostgreSQL user superuser_name.
    db_host: The name of the database host.
    db_port: The port of the database.
    poi_db_name: The name of the database in which the markers table is present.
    poi_user_name: The name of the user to be given the grants.
    '''
    try:
        logging.info("Connecting to database %s as user postgres on host %s port %s", poi_db_name, db_host, db_port) 
        connection = psycopg2.connect(
            dbname = poi_db_name,
            user = superuser_name,
            password = superuser_password,
            host = db_host,
            port = db_port)

        connection.autocommit = True
        cursor = connection.cursor()

        logging.info("Granting SELECT, INSERT and DELETE to user %s", poi_user_name)
        query = '''
            GRANT
            SELECT, INSERT, DELETE
            ON markers
            TO %s;'''
        params = (AsIs(poi_user_name),)
        cursor.execute(query, params)

        #Grant the user the USAGE privilege on the marker id sequence (SERIAL)
        logging.info("Granting USAGE on id sequence to user %s", poi_user_name)
        query = '''
            GRANT
            USAGE
            ON markers_id_seq
            TO %s;'''
        params = (AsIs(poi_user_name),)
        cursor.execute(query, params)

        logging.info("Successfully granted user %s", poi_user_name)
    except Exception as e:
        print("Error giving user grants", e)
