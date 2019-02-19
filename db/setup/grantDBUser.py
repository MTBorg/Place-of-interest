import psycopg2
from psycopg2.extensions import AsIs

def grant_dbuser(existing_db_superuser_name, existing_db_superuser_pass, host_name, host_port, db_name, dbuser_name):
    '''Connects to the specified database and gives the specified
    user grants to the markers table

    Parameters
    ----------
    existing_db_superuser_name = A existing superuser that has the power to careate a new database.
    existing_db_superuser_pass: Password of the default PostgreSQL user existing_db_superuser_name.
    host_name: The name of the database host.
    host_port: The port of the database.
    db_name: The name of the database in which the markers table is present.
    dbuser_name: The name of the user to be given the grants.
    '''
    try:
        connection = psycopg2.connect(
            dbname = db_name,
            user = existing_db_superuser_name,
            password = existing_db_superuser_pass,
            host = host_name,
            port = host_port)

        connection.autocommit = True
        cursor = connection.cursor()
        query = '''
            GRANT
            SELECT, INSERT, DELETE
            ON markers
            TO %s;'''
        params = (AsIs(dbuser_name),)
        cursor.execute(query, params)

        #Grant the user the USAGE privilege on the marker id sequence (SERIAL)
        query = '''
            GRANT
            USAGE
            ON markers_id_seq
            TO %s;'''
        params = (AsIs(dbuser_name),)
        cursor.execute(query, params)
    except Exception as e:
        print("Error giving user grants", e)