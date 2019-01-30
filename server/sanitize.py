import bcrypt, datetime

class Sanitizer(object):

    __SECRET_STR = b"123"

    def  __init__(self):
        pass

    def getHashCookie(self):
        cookieHash = bcrypt.hashpw(self.__SECRET_STR, bcrypt.gensalt())
        return cookieHash

    def checkHashCookie(self, cookieHash):
        cookieHash = cookieHash.encode('utf-8')
        if(bcrypt.checkpw(self.__SECRET_STR, cookieHash)):
            return True
        else:
            return False

    def checkTimeCookie(self, cookieTime):
        print(cookieTime, " haha ")
        
