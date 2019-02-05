from flask import Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os   

app = Flask(__name__, template_folder=".")
#path from where this file is executed.
path = os.path.dirname(os.path.realpath(__file__))

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
    #What icon to show on map (flagged location & current location of user).
    flaggedLocationsIcon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png" #http://maps.google.com/mapfiles/ms/icons/blue-dot.png
    currentLocationIcon = "http://maps.google.com/mapfiles/dir_0.png"
    #lng & lat for positions to show.
    flaggedLocations = [(65.621650, 22.117025, "Vänortsvägen"), (65.618776, 22.139475, "E-huset"), (65.618929, 22.051285, "Storheden")]
    #marks which combine the icon and flaggedLocations.
    marks = []
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
        lat = request.form["lat"]
        lng = request.form["lng"]
        marks.append({
            "icon": flaggedLocationsIcon,
            "lat": lat,
            "lng": lng,
            "infobox": "Current location",
        })

    #render the map for HTML
    sndmap = Map(
        identifier="sndmap",
        lat=65.618776,
        lng=22.139475,
        markers=marks,
        style=(
            "height:94%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position: absolute;"
            "z-index:200;"
        ),
        zoom=16 ,
        center_on_user_location=True
    )
    return render_template('./templates/index.html', sndmap=sndmap)
@app.route("/settings")
def settignsView():
    return render_template('./templates/settings.html')


if __name__ == "__main__":
    app.run(debug=True)
