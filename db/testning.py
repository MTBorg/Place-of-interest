import sys
# Add the parent folder path to the sys.path list
sys.path.insert(0,'setup')
import setup.runSetupFiles as setup
import db

import datetime


#setup.run()
db = db.db()
db.save_marker(40.00001,20.00001, "2")
api_return = db.get_markers_from_userid("2")
#print(api_return)
api_return1 = db.get_markers_from_dist(40, 20, 10000)
#print(api_return1)

start = datetime.datetime(2019, 1, 31, 0, 0, 0, 0)  
end = datetime.datetime(2019, 2, 1, 0, 0, 0, 0)  
api_return2 = db.get_markers_from_distTime(40, 20, 10000, start,end)

print(api_return2)