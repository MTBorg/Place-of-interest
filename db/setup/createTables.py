import psycopg2

def createTables(dbname, username, hostname, password, portnr):
    """Create tables in database

    This script creates one table in the database for storing markers.

    Parameters
    ----------
    dbname: Name of the database to connect to
    username: Name of the PostgreSQL user for the database
    hostname: Name/address of database host
    password: Password of the default PostgreSQL user (postgres)
    portnr: Port of the host that the database listens to
    """
    try:
        connection = psycopg2.connect(dbname=dbname, user=username, host=hostname, password=password, port=portnr)
        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute("CREATE SEQUENCE marker_seq")
        SQL = "CREATE TABLE Markers(id INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('marker_seq'), marker geography(POINT, 4326), created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, user_id VARCHAR(255) NOT NULL)"
        cursor.execute(SQL)
    except Exception as e:
        print("Exception creating tables:", e)

