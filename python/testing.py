from opensky_api import OpenSkyApi
from keys import idpassword

import pandas as pd
id, password = idpassword
api = OpenSkyApi(id,password)

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson

def getFlightBox(bbox=(1, 2, 100.97, 104.3)):
	s = api.get_states(bbox=bbox)
	ds = str(s).replace("   ","")
	#print("In raw form, states and time are:",ds)
	return ds
	
states = getFlightBox()
print("Processing...\n")
'''Building 2 functions to fit API outputs...'''
def StateVector(data):
	return data
def dict_values(data):
	return data

'''Parsing into Pandas DataFrame'''
processed = eval(states)
flights = processed['states']
time = processed['time']

dfflight = pd.DataFrame(flights,\
columns=['icao24','callsign','origin_country','time_position','last_contact','longitude',\
'latitude','geo_altitude','on_ground','velocity','true_track','vertical_rate','sensors',\
'baro_altitude','squawk','spi','position_source','category'])

cols = ['icao24','callsign','origin_country','time_position','last_contact',\
'geo_altitude','on_ground','velocity','true_track','vertical_rate','sensors',\
'baro_altitude','position_source','category']
    
print("Done evaluating data in Python. Printing DataFrame:")
dfflight = dfflight.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
print(dfflight.head())

print("Check: dfflight is of type",type(dfflight))


geojson = df_to_geojson(dfflight, cols)
import contextily
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopandas import GeoDataFrame
''' Tutorial from https://www.datacamp.com/tutorial/geopandas-tutorial-geospatial-analysis '''


geometry = [Point(xy) for xy in zip(dfflight.longitude, dfflight.latitude)]
gdf = GeoDataFrame(dfflight, geometry=geometry)

gdf.set_crs(epsg=4326, inplace=True)


ax2= gdf.plot(figsize=(12,12), legend=True)

# flight_geojson["centroid"].plot(ax=ax, color="green")

contextily.add_basemap(ax2,crs=gdf.crs.to_string())
plt.title('Flights Around Changi')
plt.axis('off')
plt.savefig('Flights WSSS', dpi=300)
plt.show()

'''Other codes (Future works)'''
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