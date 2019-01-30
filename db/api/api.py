import psycopg2

def get_markers_from_dist(db, origin, radius):
    '''Retrieves all markers within a given circle

    Parameters
    ----------
    connection - Cursor for open connection
    origin - The center of the circle
    radius - The radius of the circle

    Returns
    -------
    A list containing all markers within the given circle 
    '''
    cursor = db.connect()
    query = "SELECT marker FROM MARKERS WHERE ST_DWithin(%s, marker, %s)"
    data = (origin, radius)
    cursor.execute(query, data)

    return cursor.fetchall()
    

def get_markers_from_distTime(connection, origin, radius, startTime, endTime):
    '''Retrieves all markers within a given circle and within a given time interval

    Parameters
    ----------
    origin - The center of the circle
    radius - The radius of the circle
    startTime - The start of the time interval
    endTime - The end of the time interval

    Returns
    -------
    A list containing all markers within the given circle and time interval
    '''
    cursor = connection

    query = "SELECT marker FROM MARKERS WHERE ST_DWithin(%s, marker, %s) AND %s <= created_at AND %s >= created_at AND"

    data = (origin, radius, startTime, endTime)

    cursor.execute(query, data)

    return cursor.fetchall()

def get_markers_from_userId(db, user_id):
    '''Retrieves all markers associated with a given user id

    Parameters
    ----------
    user_id - The id of the user

    Returns
    -------
    A list of tuples of form (longtiude, latitude) associated with the user
    '''
    cursor = db.connect()
    query = "SELECT ST_X(ST_AsEWKT(marker)), ST_Y(ST_AsEWKT(marker)) FROM markers WHERE userid=%s;"
    cursor.execute(query, user_id)
    return cursor.fetchall()
    

def save_marker(db, lng, lat, user_id):
    '''Stores a given point in the database

    Parameters
    ----------
    connection - Connection to database
    lng - Longitude of marker position
    lat - Latitude of marker position
    user_id - The id of the user

    Returns
    -------
    True if point was succesfully stored in the database, otherwise False
    '''
    cursor = db.connect()
    coordinates = "POINT(%s %s)" % (lng, lat)
    query = "INSERT INTO markers (marker, user_id) VALUES (ST_GeomFromText(%s, 4326), %s)"
    data = (coordinates, user_id)
    cursor.execute(query, data)