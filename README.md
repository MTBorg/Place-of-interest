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

Database setup file and connection requirements:
* A database name, that can be change in the data.json file.
* The username for the default postgresql database.
* A hostname.
* The password for the default postgresql database.
* A port.
* A read/write username and password. (Can also be the default postgresql user, but it is not recommended.)

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
