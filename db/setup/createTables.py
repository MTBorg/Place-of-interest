import psycopg2
import logging

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
        logging.info("Connecting to database %s as user %s on host %s port %s", poi_db_name, poi_user_name, db_host, db_port)
        connection = psycopg2.connect(dbname=poi_db_name, user=poi_user_name, host=db_host, password=poi_user_password, port=db_port)

        connection.autocommit=True
        cursor = connection.cursor()
        
        #Create the table
        logging.info("Creating table markers")
        query = "CREATE TABLE Markers(id SERIAL PRIMARY KEY, marker geography(POINT, 4326), created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, user_id VARCHAR(255) NOT NULL)"
        cursor.execute(query)
    
        #Create indices
        logging.info("Creating indices for table markers")
        cursor.execute("CREATE INDEX ON markers (user_id)")
        
        #Close connections
        logging.info("Closing connection")
        cursor.close()
        connection.close()        

        logging.info("Succesfully created table markers")
    except psycopg2.Error as e:
        if e.pgcode == '42P07': #duplicate_table code
            logging.warning("Table markers already exists. Make sure it has the correct attributes or delete it and run the setup script again")
        else:
            raise Exception("Exception creating table markers: " + str(e))
    except Exception as e:
        raise Exception("Exception creating table markers: " + str(e))

