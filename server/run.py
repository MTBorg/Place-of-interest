from flask import Flask, render_template, request, jsonify, make_response
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os, sys, sanitize, datetime

app = Flask(__name__, template_folder=".")
#path from where this file is executed.
path = os.path.dirname(os.path.realpath(__file__))

#sanitizie
sanitizer = sanitize.Sanitizer()

#What icon to show on map (flagged location & current location of user).
flaggedLocationsIcon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png" #http://maps.google.com/mapfiles/ms/icons/blue-dot.png
currentLocationIcon = "http://maps.google.com/mapfiles/dir_0.png"

#marks which combine the icon and flaggedLocations.
marks = []

#read in the google maps API key
try:
    f = open(os.path.realpath(path+"/api_key/key.txt"), "r") #text file with your API key
except IOError:
    print("Couldn't fetch key for google maps API from "+path)
else:
    key = f.read()
    app.config['GOOGLEMAPS_KEY'] = key
    f.close()

GoogleMaps(app)

@app.route("/", methods=['GET', 'POST'])
def mapview():
    #lng & lat for positions to show.
    flaggedLocations = [(65.621650, 22.117025, "Vänortsvägen"), (65.618776, 22.139475, "E-huset"), (65.618929, 22.051285, "Storheden")]
    #append the marks to marks list so we can render them into the map.
    for i in range(len(flaggedLocations)):
        marks.append({
            "icon": flaggedLocationsIcon,
            "lat": flaggedLocations[i][0],
            "lng": flaggedLocations[i][1],
            "infobox": flaggedLocations[i][2],
        })

    #If there's a POST to the site.
    if request.method == "POST":
        if("hash" in request.cookies and sanitizer.checkHashCookie(request.cookies.get("hash"))):
            if(sanitizer.checkTimeCookie(request.cookies.get("time"))):
                addMark(request.form["lat"], request.form["lng"])
                response = make_response(render_template('./templates/index.html', sndmap=renderMap()))
                response.set_cookie("time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                print(marks)
                return render_template('./templates/index.html', sndmap=renderMap())
        else:
            addMark(request.form["lat"], request.form["lng"])
            response = make_response(render_template('./templates/index.html', sndmap=renderMap()))
            response.set_cookie("hash", sanitizer.getHashCookie())
            response.set_cookie("time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response
    return render_template('./templates/index.html', sndmap=renderMap())


#add a marker to the map
def addMark(lat, lng):
    marks.append({
        "icon": flaggedLocationsIcon,
        "lat": lat,
        "lng": lng,
        "infobox": "Current location",
    })

def renderMap():
    #render the map for HTML
    sndmap = Map(
        identifier="sndmap",
        lat=65.618776,
        lng=22.139475,
        markers=marks,
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position: absolute;"
            "z-index:200;"
        ),
        zoom=14,
        center_on_user_location=True
    )
    return sndmap

if __name__ == "__main__":
    app.run(debug=True)
