import psycopg2
from psycopg2.extensions import AsIs


def create_dbuser(existing_db_name, existing_db_superuser_name, existing_db_superuser_pass, host_name, host_port, new_db_user_name, new_db_user_pass):

    """Creates a user for access to database

    Parameters
    ----------
    existing_db_name: Database name of an existing database.
    existing_db_superuser_name = A existing superuser that has the power to careate a new database.
    existing_db_superuser_pass: Password of the default PostgreSQL user existing_db_superuser_name.
    host_name: Name/address of database host.
    host_port: Port of the host that the database listens to. 
    new_db_user_name: The name of the user to create.
    new_db_user_pass: The password for the new user.
    """
    try:
        connection = psycopg2.connect(dbname=existing_db_name, user=existing_db_superuser_name, host=host_name, password=existing_db_superuser_pass, port=host_port)
        connection.autocommit=True
        cursor = connection.cursor()
        query = '''CREATE ROLE %s WITH 
                NOSUPERUSER
                NOCREATEDB
                NOCREATEROLE
                NOINHERIT
                LOGIN
                CONNECTION LIMIT -1
                ENCRYPTED PASSWORD %s'''
        params = (AsIs(new_db_user_name), new_db_user_pass)
        cursor.execute(query, params)
    except Exception as e:
        print("Exception creating user:", e)

