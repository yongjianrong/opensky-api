from opensky_api import OpenSkyApi
from keys import idpassword
import pandas as pd
id, password = idpassword
api = OpenSkyApi(id,password)

def getFlightStates(bbox=(1, 2, 103.97, 104.3)):
	s = api.get_states(bbox=bbox)
	ds = str(s).replace("   ","")
	#print("In raw form, states and time are:",ds)
	return ds
	
states = getFlightStates()
print("Processing...\n")
'''Building 2 functions just to fit the API outputs...'''
def StateVector(data):
	return data
def dict_values(data):
	return data

processed = eval(states)

for key, val in processed.items():
	print(key,":",val)
print("Done evaluating data in Python.")

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