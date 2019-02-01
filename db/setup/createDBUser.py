import psycopg2
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
        connection = psycopg2.connect(dbname='postgres', user='postgres', host=host_name, password=psql_pass, port=host_port)
        connection.autocommit=True
        cursor = connection.cursor()
        SQL = '''CREATE ROLE %s WITH 
                NOSUPERUSER
                NOCREATEDB
                NOCREATEROLE
                NOINHERIT
                LOGIN
                CONNECTION LIMIT -1
                ENCRYPTED PASSWORD %s'''
        data = (AsIs(dbuser_name), dbuser_pass)
        cursor.execute(SQL, data)
    except Exception as e:
        print("Exception creating user:", e)
