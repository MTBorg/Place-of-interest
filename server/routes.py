from flask import Flask, render_template
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
    app.config['GOOGLEMAPS_KEY'] = f.read()
    f.close()

GoogleMaps(app)

@app.route("/")
def mapview():
    #What icon to show on map (flagged location)
    icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png" #http://maps.google.com/mapfiles/ms/icons/blue-dot.png
    #lng & lat for positions to show.
    flaggedLocations = [(65.621650, 22.117025, "Vänortsvägen"), (65.618776, 22.139475, "E-huset"), (65.618929, 22.051285, "Storheden")]
    #marks which combine the icon and flaggedLocations
    marks = []
    for i in range(len(flaggedLocations)):
        marks.append({
            "icon": icon,
            "lat": flaggedLocations[i][0],
            "lng": flaggedLocations[i][1],
            "infobox": flaggedLocations[i][2],
        })
    #render the map for HTML
    sndmap = Map(
        identifier="sndmap",
        lat=65.618776,
        lng=22.139475,
        markers=marks,
        style="height: 700px; width: 1200px;",
        zoom=12,
    )
    return render_template('./templates/index.html', sndmap=sndmap)

if __name__ == "__main__":
    app.run(debug=True)
