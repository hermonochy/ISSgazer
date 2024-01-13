import sys
sys.path.append("../modules/orbit-predictor/")
from orbit_predictor.sources import EtcTLESource
from orbit_predictor.locations import Location

OXFORD = Location(
    "OXFORD", latitude_deg=-1.20187, longitude_deg=51.75524, elevation_m=26.00)

source = EtcTLESource(filename="trajectorydata/240111iss.tle")
predictor = source.get_predictor("ISS")

predicted_pass = predictor.get_next_pass(OXFORD)


print(predicted_pass)

position = predictor.get_position(predicted_pass.aos)

OXFORD.is_visible(position)  # Can I see the ISS from this location?
#True

import datetime

position_delta = predictor.get_position(predicted_pass.los + datetime.timedelta(minutes=20))

OXFORD.is_visible(position_delta)
#False

tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)

predictor.get_next_pass(OXFORD, tomorrow, max_elevation_gt=20)

