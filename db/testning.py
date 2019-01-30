import sys
# Add the parent folder path to the sys.path list
sys.path.insert(0,'setup')
import setup.runSetupFiles as setup

import api.api as api 
import db

setup.run()
db_var = db.db()
api.save_marker(db_var, 40,20, "1")
api_return = api.get_markers_from_userId(db_var, "1")
print(api_return)
api_return1 = api.get_markers_from_dist(db_var, ST_GeomFromText("POINT(40 20)", 4326), 10000)
print(api_return1)
api_return1 = api.get_markers_from_distTime(db_var, ST_GeomFromText("POINT(40 20)", 4326), 10000, ,)
print(api_return2)