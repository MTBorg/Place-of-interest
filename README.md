# Contributors
* Henrik Ingstorp, hening-6@student.ltu.se
* Niklas Lundberg, inaule-6@student.ltu.se
* Tim Coull, timcou-6@student.ltu.se
* Andreas Månsson, andmns-5@student.ltu.se
* Ida Lundberg, lunida-1@student.ltu.se
* Johan Delissen, johdel-5@student.ltu.se
* Martin Terneborg, termar-5@student.ltu.se

# Prerequisites
* Python 3.6 + pip
* Flask 1.0.2
* Postgresql 10.6
* PostGis 2.5.1
* Google Maps API Key



# Database 
All the files that are related to the database are in the db folder. The setup folder in there is for setting up a postgresql database that has all the basic functionality for the PoI application. There is also a json setup file in the setup folder, that can be used to change some key variables of the database. The db.py file is a api for establishing a connection to the database and defining the queries.

# Database requirements
Database schemas requirements:
* A table named markers.

Table markers requirements:
* A column named id of type integer, that is primary key and can't be null.
* A column named marker of type geography, that is not null.
* A column named created_at of type timestamp with time zone, that can't be null.
* A column named user_id of type character varying (255), that can't be null.
* A column named ip_address of type character varying (255), that can't be null.

Database setup requirements(Only needed if running the setup script in the setup folder):
* A default postgresql database name. (The database that is requierd to be made when instaling postgresql)
* A default postgresql username and password. (The user that is requierd to be made when instaling postgresql)

# Setting up the database
In the db folder there is a folder named setup, in there there is a file called "data.json". The first thing is to open the json file and change the keys value. 

This list describes what the connection keys are:
* dbname: The database name.
* user: The username for the default postgresql database.
* host: The host name.
* password: The password for the default postgresql database.
* port: The port number for the database.

This list describes what the user keys are:
* username: The username for a new user, that can only read and write to the database.
* password: The password for a new user, that can only read and write to the database.

After the json file is filled in with the right data, the next step is to run the "runSetupFiles.py" file. That file can be found in the setup folder that is in the db folder. When running this file make sure that the directory you are in is "../D0020E/db/setup", otherwise there can be an error. After running the python file the database plus the user should be setup and ready to go.

# Changing database
The new database needs to follow the database requirements that are listed under "Database requirements", this is to assure that no problems appear. If the new database has different tables and/or columns the application will probably not work and manuel changes all over the code is required. To run queries on the new database, the db.py file in the db folder needs to be updated so that the database code works on the new database. Under the header "Database queries" there is more information on how the queries work.

# Database queries and connection
All the queries for the database are located in the db.py file in the db folder. The query functions take in specific parameters that shouldn't be changed because they are used in other places of the application. If they need to be changed then that has to be manually done all over the code. To just change the queries the variable "query" is the only thing that needs changing and it should work. In the query functions there are also some code for establishing and closing a connection to the database, this should not need changing.

The db class constructor reads the connection and user data from the data.json and saves it in local variables. Then the db object is used in the backend part of the application to communicate to the database. In the object there is a function called "__connect()"  that should only be used locally in the db object and is for making a connection to the database. The connection is then closed in the query functions after the query is executed.

