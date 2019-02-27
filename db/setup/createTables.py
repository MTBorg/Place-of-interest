import psycopg2

def create_tables(poi_user_name, poi_user_password, db_host, db_port, poi_db_name,):
    """Create tables in database

    This script creates one table in the database for storing markers.

    Parameters
    ----------
    poi_user_name: Name of the PostgreSQL user for the database.
    poi_user_password: poi_user_Password of the default PostgreSQL user (postgres).
    db_host: Name/address of database host.
    db_port: Port of the host that the database listens to.
    poi_db_name: Name of the database to connect to
    """
    try:
        #Connect to database
        connection = psycopg2.connect(dbname=poi_db_name, user=poi_user_name, host=db_host, password=poi_user_password, port=db_port)
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

