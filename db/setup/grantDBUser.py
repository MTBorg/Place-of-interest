import psycopg2
from psycopg2.extensions import AsIs

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
        connection = psycopg2.connect(
            dbname = poi_db_name,
            user = superuser_name,
            password = superuser_password,
            host = db_host,
            port = db_port)

        connection.autocommit = True
        cursor = connection.cursor()
        query = '''
            GRANT
            SELECT, INSERT, DELETE
            ON markers
            TO %s;'''
        params = (AsIs(poi_user_name),)
        cursor.execute(query, params)

        #Grant the user the USAGE privilege on the marker id sequence (SERIAL)
        query = '''
            GRANT
            USAGE
            ON markers_id_seq
            TO %s;'''
        params = (AsIs(poi_user_name),)
        cursor.execute(query, params)
    except Exception as e:
        print("Error giving user grants", e)