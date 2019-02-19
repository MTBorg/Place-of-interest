import psycopg2

def create_tables(username, password, hostname, portnr, dbname,):
    """Create tables in database

    This script creates one table in the database for storing markers.

    Parameters
    ----------
    username: Name of the PostgreSQL user for the database.
    password: Password of the default PostgreSQL user (postgres).
    hostname: Name/address of database host.
    portnr: Port of the host that the database listens to.
    dbname: Name of the database to connect to
    """
    try:
        #Connect to database
        connection = psycopg2.connect(dbname=dbname, user=username, host=hostname, password=password, port=portnr)
        connection.autocommit=True
        cursor = connection.cursor()
        
        #Create the table
        query = "CREATE TABLE Markers(id SERIAL PRIMARY KEY, marker geography(POINT, 4326), created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, user_id VARCHAR(255) NOT NULL, ip_address VARCHAR(255) NOT NULL)"
        cursor.execute(query)
    
        #Create indices
        cursor.execute("CREATE INDEX ON markers (user_id)")
        cursor.execute("CREATE INDEX ON markers (ip_address)")
        
        #Close connections
        cursor.close()
        connection.close()        
    except Exception as e:
        print("Exception creating tables:", e)

