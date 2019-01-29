import psycopg2

class db():

    def __init__(self, dbname, hostname, portnr, username, password):
        '''Setup a database object

        Parameters
        ----------
        dbname - Name of the database to setup connection for
        hostname - Name/address of database host
        portnr - Port of the host that the database listens to
        username - Name of the user with read/write access to database
        password - Password for the given user

        '''
        self.dbname = dbname
        self.hostname = hostname
        self.portnr = portnr
        self.username = username
        self.password = password



    def connect(self):
        ''' Try to connect to database

        Returns
        -------
        Connection to database if no exception
        '''
        try:
            connection = psycopg2.connect(dbname=self.dbname, host=self.hostname, port=self.portnr, user=self.username, password=self.password)
            connection.autocommit=True
            return connection.cursor()
        except Exception as e:
            print("Failed to connect to database:", e)