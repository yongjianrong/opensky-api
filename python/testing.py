from opensky_api import OpenSkyApi
api = OpenSkyApi()

# SKW4734 at 1.42am on 28/7/2023
s = api.get_states(icao24='aa8c10')
print(s)

# arrivals = api.get_arrivals_by_airport('WMKK',1690470000,1690478600)
arrivals = api.get_flights_from_interval(1690470000,1690470010)
print(arrivals)