import psycopg2
import logging

def create_tables(dbname, username, hostname, password, portnr):
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
        #Connect to database
        logging.info("Connecting to database %s as user %s on host %s port %s", dbname, username, hostname, portnr)
        connection = psycopg2.connect(dbname=dbname, user=username, host=hostname, password=password, port=portnr)
        connection.autocommit=True
        cursor = connection.cursor()
        
        #Create the table
        logging.info("Creating table markers")
        query = "CREATE TABLE Markers(id SERIAL PRIMARY KEY, marker geography(POINT, 4326), created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, user_id VARCHAR(255) NOT NULL, ip_address VARCHAR(255) NOT NULL)"
        cursor.execute(query)
    
        #Create indices
        logging.info("Creating indices for table markers")
        cursor.execute("CREATE INDEX ON markers (user_id)")
        cursor.execute("CREATE INDEX ON markers (ip_address)")
        
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

