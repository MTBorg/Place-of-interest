import psycopg2
import logging
from psycopg2.extensions import AsIs


def create_dbuser(default_db_name, superuser_name, superuser_password, db_host, db_port, poi_user_name, poi_user_password):

    """Creates a user for access to database

    Parameters
    ----------
    default_db_name: Database name of an existing database.
    superuser_name = A existing superuser that has the power to careate a new database.
    superuser_password: Password of the default PostgreSQL user superuser_name.
    db_host: Name/address of database host.
    db_port: Port of the host that the database listens to. 
    poi_user_name: The name of the user to create.
    poi_user_password: The password for the new user.
    """
    try:
        logging.info("Connecting to database postgres as user postgres at host %s port %s", db_host, db_port)
        connection = psycopg2.connect(dbname=default_db_name, user=superuser_name, host=db_host, password=superuser_password, port=db_port)

        connection.autocommit=True
        cursor = connection.cursor()

        logging.info("Creating role %s", poi_user_name)
        query = '''CREATE ROLE %s WITH 
                NOSUPERUSER
                NOCREATEDB
                NOCREATEROLE
                NOINHERIT
                LOGIN
                CONNECTION LIMIT -1
                ENCRYPTED PASSWORD %s'''
        params = (AsIs(poi_user_name), poi_user_password)
        cursor.execute(query, params)

        logging.info("Successfully created user %s", poi_user_name)
    except psycopg2.ProgrammingError as e:
        if e.pgcode == '42710': #duplicate_object error code
            logging.warning("Role %s already exists. Make sure it has the necessary privileges or delete it and run the setup script again", poi_user_name)
        else:
            raise Exception("Exception creating user" + poi_user_name + ": " + str(e))
    except Exception as e:
        raise Exception("Exception creating user:" + str(e))

