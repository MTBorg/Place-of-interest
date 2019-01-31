import sys
# Add the parent folder path to the sys.path list
sys.path.insert(0,'setup')
import setup.runSetupFiles as setup
import db

setup.run()
db = db.db()
db.save_marker(40,20, "1")
api_return = db.get_markers_from_userid("1")
print(api_return)
#api_return1 = api.get_markers_from_dist(db_var, ST_GeomFromText("POINT(40 20)", 4326), 10000)
#print(api_return1)
#api_return1 = api.get_markers_from_distTime(db_var, ST_GeomFromText("POINT(40 20)", 4326), 10000, ,)
#print(api_return2)