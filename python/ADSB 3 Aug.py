from opensky_api import OpenSkyApi
from keys import idpassword
import sys
import pandas as pd
myid, password = idpassword
api = OpenSkyApi(myid,password)
api2 = OpenSkyApi()

''' Defaults for getting time '''
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
hour = eval(current_time[0:2])
print("Current Time =", current_time)
print("Hour:", hour)

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

def getFlightBox(bbox=(1.0, 1.5, 103.9, 104.1)):
    s = api.get_states(bbox=bbox)
    # t = api.get_arrivals_by_airport("WSSS", 1690688043, 1690691043)
    # if t == None:
    #     sys.exit("None output was obtained.")
    ds = str(s).replace("   ","")
    print("In raw form, states and time are:",ds)
    return ds

# State 1: Get flights within a box
latwidth = 0.4 + 1-hour/24
lonwidth = 0.4 + 1-hour/24

latleft = 1.0
latright = latleft+latwidth
lonleft = 103.8
lonright = lonleft+lonwidth
states = getFlightBox(bbox=(latleft,latright, lonleft, lonright))

# State 2: Get Flights by Airport (NOT WORKING)
# t = api2.get_arrivals_by_airport("WSSS", 1690821545, 1690822545)
#print("Trying out ")
#print(t)
print("Processing...\n")
'''Building 2 functions to fit API outputs...'''
def StateVector(data):
	return data
def dict_values(data):
	return data

def getAircraftTrack(aircraft):
    print("For SIA221 2 Aug:")
    v = api.get_track_by_aircraft(aircraft) #SIA221 2 Augg
    trackcols = ['timestamp','latitude','longitude','altitude','track','state']
    print(v)
    dv = str(v).replace("   ","")
    dv_processed = eval(dv)
    try:
        traject = dv_processed['path']
    except TypeError as err:
        print(err,"No flight data found.")
        sys.exit()
        
    df_traject = pd.DataFrame(traject,columns=trackcols)
    print("Processed dv Df is:\n",df_traject)
    return df_traject

aircraft1 = '76cd72'
'''Function 1: Get Aircraft Track by ICAO24 Code'''
#getAircraftTrack(aircraft1)
'''Function 2: Get all flights within box'''
print(f"Getting all flights from {lonleft},{latleft} to {lonright},{latright}")
processed = eval(states)
flights = processed['states']
if len(flights) == 0:
    sys.exit("No states obtained.")
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


# geojson = df_to_geojson(dfflight, cols)
import contextily
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopandas import GeoDataFrame
''' Tutorial from https://www.datacamp.com/tutorial/geopandas-tutorial-geospatial-analysis '''

'''Form the x-y coordinates'''
geometry = [Point(xy) for xy in zip(dfflight.longitude, dfflight.latitude)]
gdf = GeoDataFrame(dfflight, geometry=geometry)
# EPSG:4326 - WGS 84, latitude/longitude coordinate system 
# based on the Earth's center of mass, used by the Global Positioning System
gdf.set_crs(epsg=4326, inplace=True) #Coord Ref System

'''Plot the GeoDataFrame'''
ax2= gdf.plot(figsize=(10,10), legend=True)
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, dfflight.callsign):
    ax2.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

contextily.add_basemap(ax2,crs=gdf.crs.to_string())
plt.title('Flights Around Changi')
plt.axis('off')
plt.savefig('Flights WSSS', dpi=250)
plt.show()
print("Plotted successfully")

'''Other codes (Future works)'''
arrivals = api.get_arrivals_by_airport('WSSS',1690550000,1690558600)
for item in arrivals:
	print(item)
# # arrivals = api.get_flights_from_interval(1690550000,1690550010)

# #print(arrivals)

# #wsss_arrivals = api.get_arrivals_by_airport('KJFK',1690480000,1690488600)
# #print(wsss_arrivals)

# # bbox = (min latitude, max latitude, min longitude, max longitude)
# #states = api.get_states(bbox=(1, 2, 103.97, 104.1))
# #for s in states.states:
#    print("(%r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity))

flights = api.get_flights_by_aircraft("76cef0",1690994209,1690994709)