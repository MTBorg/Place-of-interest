import psycopg2
from psycopg2.extensions import AsIs

def dropDatabase(db_name, host_name, host_port, su_name, su_pass):
    connection = psycopg2.connect(
        dbname = 'postgres',
        user = su_name,
        password = su_pass,
        host = host_name,
        port = host_port
    )
    connection.autocommit = True
    cursor = connection.cursor()

    query = "DROP DATABASE %s;"
    params = (AsIs(db_name),)
    cursor.execute(query, params)

def dropUser(host_name, host_port, su_name, su_pass, user_name):
    connection = psycopg2.connect(
        dbname = 'postgres',
        user = su_name,
        password = su_pass,
        host = host_name,
        port = host_port,
    )
    connection.autocommit = True
    cursor = connection.cursor()

    query = "DROP ROLE %s;"
    params = (AsIs(user_name),)
    cursor.execute(query, params)