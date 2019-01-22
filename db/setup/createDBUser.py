import psycopg2

def createDBUser():
    try:
        connection = psycopg2.connect(
                "dbname='postgres' user='postgres' host='localhost' password='123' port='5432'")
        connection.autocommit=True
        cursor = connection.cursor()
        SQL = "CREATE USER admin WITH ENCRYPTED PASSWORD %s"
        data = ("password")
        cursor.execute(SQL, data)
    except Exception as e:
        print("Exception:", e)