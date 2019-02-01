import bcrypt, datetime
from flask import Flask, render_template, request, jsonify, make_response
import controller

class Sanitizer(object):

    __SECRET_STR = b"123"
    __TIME_BETWEEN_POSTS = 10 #seconds

    def  __init__(self):
        self.__SECRET_STR = b"123"
        self. __TIME_BETWEEN_POSTS
        self.controller = controller.Controller()
        pass


    def process_request(self):

        if("hash" in request.cookies and self.checkHashCookie(request.cookies.get("hash"))):
            if(self.checkTimeCookie(request.cookies.get("time"))):
                return 0
            else:
                return 1
        else:
            return self.getHashCookie()



    def getHashCookie(self):
        '''Retrieves a hash for the cookie to be stored client-side.

        Returns
        -------
        A hash for client-side cookie.
        '''
        self.controller.saveMarker()
        cookieHash = bcrypt.hashpw(self.__SECRET_STR, bcrypt.gensalt())
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
        
