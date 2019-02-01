import sys
# Add the parent folder path to the sys.path list
sys.path.insert(0,'setup')
import setup.runSetupFiles as setup
import db

import datetime

setup.run()
db = db.db()

insert = db.save_marker(40.00001, 20.00001, "aaRHER33WEF/#w", "127.0.0.1")
if (insert == True):
	print("Marker successfully saved")
else:
	print("Failed when saving marker into database")

from_id = db.get_markers_from_userid('aaRHER33WEF/#w')
print("From user id ", from_id)

from_ip = db.get_markers_from_ip("127.0.0.1")
print("From user id ", from_ip)

from_dist = db.get_markers_from_dist(40, 20, 10000)
print("From distance ", from_dist)

start = datetime.datetime(2019, 1, 31, 0, 0, 0, 0)  
end = datetime.datetime(2019, 2, 10, 0, 0, 0, 0)  
from_dist_time = db.get_markers_from_dist_time(40, 20, 10000, start, end)
print("From time and distance ", from_dist_time)