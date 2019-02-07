import bcrypt, datetime

class Sanitizer(object):

    __SECRET_STR = b"123"
    __TIME_BETWEEN_POSTS = 120 #seconds

    def  __init__(self):
        pass

    def getHashCookie(self):
        '''Retrieves a hash for the cookie to be stored client-side.

        Returns
        -------
        A hash for client-side cookie.
        '''
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
        
