import bcrypt, datetime
from flask import Flask, render_template, request, jsonify, make_response
import controller

class Sanitizer(object):

    __SECRET_STR = b"123"
    __TIME_BETWEEN_POSTS = 60 #seconds

    def  __init__(self):
        self.__SECRET_STR = b"123"
        self. __TIME_BETWEEN_POSTS
        self.controller = controller.Controller()
        pass


    def process_request(self):
        """
        This function will take the request from the fronter-end Run.py and depending on how the
        cookie looks like give a return. Now it looks rather naked but more is to be implemented


        :return:
        Either 0 or 1, this is to check if the time of the cookie is valid or invalid
        Otherwise we return a we get a cookie with a hash that is returnes to be sent in the responce.

        """

        if("hash" in request.cookies and self.checkHashCookie(request.cookies.get("hash"))):
            if(self.checkTimeCookie(request.cookies.get("time"))):

                self.controller.saveMarker(request.form["lng"], request.form["lat"], request.remote_addr, request.cookies.get("hash"))
                return 0
            else:

                return 1
        else:
            return self.getHashCookie(request.remote_addr, request.form["lng"], request.form["lat"])



    def getHashCookie(self,ip, lng, lat):
        '''Retrieves a hash for the cookie to be stored client-side.
           Because this is a new user, we add the location and IP to the database
        Returns
        -------
        A hash for client-side cookie.
        '''
        cookieHash = bcrypt.hashpw(self.__SECRET_STR, bcrypt.gensalt())

        self.controller.saveMarker(lng, lat, ip, cookieHash)

        return cookieHash




    def checkHashCookie(self, cookieHash):
        '''Checks the clients hash against the secret string

        Parameters
        ----------
        cookieHash - the hash in the clients cookie.

        Returns
        -------
        True or False - if the hash is matching the string or not.
        '''
        cookieHash = cookieHash.encode('utf-8')
        if(bcrypt.checkpw(self.__SECRET_STR, cookieHash)):
            return True
        else:
            return False

    def checkTimeCookie(self, cookieTime):
        '''Checks when the client last added a mark

        Parameters
        ----------
        cookieTime - the time client last added a mark

        Returns
        -------
        True or False - if the client has waited enough time -> true, else -> false.
        '''
        cookieTime = datetime.datetime.strptime(cookieTime, "%Y-%m-%d %H:%M:%S")
        if(datetime.datetime.now()-cookieTime >= datetime.timedelta(seconds=self.__TIME_BETWEEN_POSTS)):
            return True
        else:
            return False



    def get_markers_by_radius(self,lat, lng, radius):
        return self.controller.getMarkersAroundLocation(lat, lng, radius)

        
