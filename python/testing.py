from opensky_api import OpenSkyApi
from keys import idpassword
id, password = idpassword
api = OpenSkyApi(id,password)

# SKW4734 at 1.42am on 28/7/2023
s = api.get_states()
f = open("states.csv", "w")
f.write(s)
f.close()
#arrivals = api.get_arrivals_by_airport('WSSS',1690470000,1690478600)
#for item in arrivals:
#	print(item)
# arrivals = api.get_flights_from_interval(1690470000,1690470010)

#print(arrivals)

#wsss_arrivals = api.get_arrivals_by_airport('KJFK',1690480000,1690488600)
#print(wsss_arrivals)

# bbox = (min latitude, max latitude, min longitude, max longitude)
#states = api.get_states(bbox=(1, 2, 103.97, 104.1))
#for s in states.states:
#    print("(%r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity))