import sys, bcrypt,os, inspect, datetime
from flask import Flask, jsonify, make_response

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir) + "/db/"
sys.path.insert(0,parentdir)

import db as database
import sanitize

class Controller:

    def __init__(self):
        #create database connection instance to use for db calls.
        self.db = database.db()
        self.DEFAULT_RADIUS = 100000000
        self.Sanitizer = sanitize.Sanitizer()

    def createQuery(self, request):
        """
        Here we create the query for the
        :param request: the request with the informatino needed to create the querry,
        :param cookiedata: Cookiedata given from santizier
        :return: The query of the database
        """
        if(request.form['request-specification'] == "FetchMarkers"):
            resultOnReturn = self.getMarkersAroundLocation(request.form['lng'], request.form['lat'], 120000)
            return make_response(jsonify(resultOnReturn))

        if request.form["request-specification"] == "SetMarker":
            check = self.Sanitizer.cookieCheck(request)
            if(check == True):
                self.db.save_marker(request.form["lng"], request.form["lat"], request.remote_addr, request.cookies.get("hash"))
                response = make_response(jsonify(["Marker set"]))
                response.set_cookie("time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expires=datetime.datetime.now() + datetime.timedelta(days=30))
                return response
            elif(check == False):
                return make_response(jsonify(["Wait a little longer before putting down marker."]))
            else:
                response = make_response(jsonify("Marker set, made new cookie"))
                response.set_cookie("hash", self.Sanitizer.getHashCookie(), expires=datetime.datetime.now() + datetime.timedelta(days=30))
                response.set_cookie("time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expires=datetime.datetime.now() + datetime.timedelta(days=30))
                return response


        if request.form["request-specification"] == "getMarkersFromTimeAndPerson":
            result =  self.getMarkersTimeSpan(request.form["lng"], request.form["lat"],
                                           request.form["start_date"],request.form["end_date"],
                                           request.form["start_time"],request.form["end_time"], self.DEFAULT_RADIUS)
            return make_response(jsonify(result))



        if request.form["request-specification"] == "Time_chosenlocation":
            return self.db.getMarkersAroundLocation(request.form["lng"], request.form["lat"],request.form["radius"])


    def getMarkersAroundLocation(self, lat, lng, radius):
        '''Retrieves all markers within a given circle from database

        Parameters
        ----------
        lat - latitude
        lng - longitude

        Returns
        -------
        A list containing all markers within the given circle 
        '''
        return self.db.get_markers_from_dist(lat, lng, radius)


    def getMarkersTimeSpan(self,lng, lat, startDate, endDate, startTime, endTime, radius):

        """
        This get the markers filtered by time

        :param lat: - latitude of current position
        :param long: - longitude of current position
        :param radius: - Radius of the position given
        :param startTime: - Filter for markers set after this time
        :param endTime: - Filter for markers set Before this time

        :return:
        --------

        Get the results from the Database
        """



        startTime = startDate + " " +startTime

        endTime = endDate + " " + endTime

        print(startTime,endTime)

        try:
            return self.db.get_markers_from_dist_time(lng, lat, radius, startTime,endTime)



        except Exception as e:
            print("Database Fault due to", e)



    def saveMarker(self, lng, lat, ip, cookieHash):
        '''Stores a given point in the database

        Parameters
        ----------
        lat - latitude of current position
        lng - longitude of current position
        ip - clients current ip
        cookieSession - session id from clients cookie

        Returns
        -------
        True if point was succesfully stored in the database, otherwise False
        '''

        try:
            self.db.save_marker(lng, lat, ip, cookieHash)

        except Exception as e:
            print("Database Fault due to", e)
