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

# Configuration

### PostgreSQL
Before making any configurations you should make backups of the default configuration files
```
cd /etc/postgresql/10/main
sudo cp postgresql.conf postgresql_backup.conf
sudo cp pg_hba.conf pg_hba_backup.conf
```
#### Scram-sha-256
By default PostgreSQL encrypts passwords using MD5, however MD5 is quite outdated and not very secure. Luckily, PostgreSQL 10 comes with scram-sha-256 which is more secure.
To scram-sha-256 encrypt the password for the default PostgreSQL:
```
sudo psql -U postgres -h <host> #Connect to PostgreSQL
SET password_encryption='scram-sha-256'; #Set the password encryption
SHOW password_encryption; #Verify password encryption is scram-sha-256
ALTER ROLE postgres WITH PASSWORD '<password>'; #Set the new password
SELECT rolname, rolpassword FROM pg_authid WHERE rolname=postgres; #Verify that the password is encrypted using scram-sha-256
```
According to the offical [PostgreSQL docs](https://www.postgresql.org/docs/10/auth-methods.html#AUTH-PASSWORD)
>To ease transition from the md5 method to the newer SCRAM method, if md5 is specified as a method in pg_hba.conf but the user's password on the server is encrypted for SCRAM (see below), then SCRAM-based authentication will automatically be chosen instead.

Thus, you should still be able to connect to the database. However you probably want to force the connecting client to use a scram-sha-256 encrypted password when connection by adding the line
```
host    all             postgres             <address/address-range>            scram-sha-256
```
Now logout as the postgres user, restart the server
```
sudo service postgresql restart
```
and make sure that you can still log in to the postgres user.
