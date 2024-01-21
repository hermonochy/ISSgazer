import datetime
import sys
sys.path.append("../modules/orbit-predictor/")
from orbit_predictor.sources import EtcTLESource
from orbit_predictor.locations import Location

OXFORD = Location(
    "OXFORD", latitude_deg=-1.20187, longitude_deg=51.75524, elevation_m=26.00)

print(OXFORD)

source = EtcTLESource(filename="../trajectorydata/240111iss.tle")
predictor = source.get_predictor("ISS")

predicted_next_pass = predictor.get_next_pass(OXFORD)
print(predicted_next_pass)


utc_nextpass = predicted_next_pass.aos
print(utc_nextpass)
#predicted_nextnext_pass = predictor.get_next_pass(OXFORD, when_utc=utc_nextpass+ datetime.timedelta(minutes=20))
#print(predicted_nextnext_pass)
predicted_following_pass = predicted_next_pass
for i in range (1,15):
   predicted_following_pass = predictor.get_next_pass(OXFORD, when_utc = predicted_following_pass.aos + datetime.timedelta(minutes = 20 ))
   position_ecef = predictor.get_position(predicted_following_pass.aos)
   position_llh = position_ecef.position_llh
   print(predicted_following_pass, position_llh)

"""


position = predictor.get_position(predicted_pass.aos)

print(position)

OXFORD.is_visible(position)  # Can I see the ISS from this location?
#True

import datetime

position_delta = predictor.get_position(predicted_pass.los + datetime.timedelta(minutes=20))

print(position_delta)

OXFORD.is_visible(position_delta)
#False

tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)

next_predicted_path_tomorrow = predictor.get_next_pass(OXFORD, tomorrow, max_elevation_gt=20)
print(next_predicted_path_tomorrow)

"""
