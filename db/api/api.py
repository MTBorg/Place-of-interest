import psycopg2

def get_markers_from_dist(origin, radius):
    '''Retrieves all markers within a given circle

    Parameters
    ----------
    origin - The center of the circle
    radius - The radius of the circle

    Returns
    -------
    A list containing all markers within the given circle 
    '''
    pass

def get_markers_from_distTime(origin, radius, startTime, endTime):
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
    pass

def get_markers_from_userId(user_id):
    '''Retrieves all markers associated with a given user id

    Parameters
    ----------
    user_id - The id of the user

    Returns
    -------
    A list containing all markers associated with the user
    '''
    pass

def save_marker(connection, lng, lat, user_id):
    '''Stores a given point in the database

    Parameters
    ----------
    point - The point to store

    Returns
    -------
    True if point was succesfully stored in the database, otherwise False
    '''
    pass