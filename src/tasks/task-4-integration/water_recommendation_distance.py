import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlite3 

# Create an engine to connect to sqlite database
engine = create_engine('sqlite:///water_points.db')
conn = engine.connect()
#conn = mysql.connector.connect('C:/Users/2039845/OneDrive - Cognizant/Desktop/Streamlit/Osun/water_points.db')
# Load the dataset from the database
df = pd.read_sql_table('etlTable', con=conn)

def distance_between_two_points(lat1, lat2, lon1, lon2):

     """
     A procedure to get the distance between two points with latitdues and longitudes
     INPUTS:
        lat1: -> latitude of the first point in degree 
        lat2: -> latitude of the second point in degree 
        lon1: -> longitude of the first point in degree 
        lon2: -> longitude of the second point in degree 
     """
     
    # The numpy module contains a function named
    # radians which converts from degrees to radians
     lat1a = np.radians(lat1)
     lat2a = np.radians(lat2)
      
    # Haversine formula
     dlon = np.radians(lon2 - lon1)
     dlat = np.radians(lat2 - lat1)
     a = np.sin(dlat / 2)**2 + np.cos(lat1a) * np.cos(lat2a) * np.sin(dlon / 2)**2
     c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
     r = 6371
      
     # calculate the result
     return np.round(c * r, 6)

def closest_taps_distance(lat, lng, dist, num_taps=10):
    """
    A procedure that recommends nearest water taps based on distance.
    INPUTS:
        df1 - water points dataframe
        num_taps - the number of water points to recommend.
    OUTPUT:
        closest_taps - a dataframe comprising location of the water points, 
        population and distance of water points from the user.
    """
    
     #Create a column for distance between a household and nearest water points
    df1 = df.copy()
    distance = []
    lat1 = float(lat)
    lon1 = float(lng)
    for row in df.itertuples(index=False):
        distance.append(distance_between_two_points(lat1, row.latitude, lon1, row.longitude) )
    
    df1['dist'] = distance
    df1 = df1[(df1.subjective_quality=="Acceptable quality") & (df1.status=="Functional (and in use)") & (df1.water_source=="Borehole")]
    closest_taps = df1.sort_values(by="dist")
    
    # Get the top points
    closest_taps = closest_taps[['location', 'population', 'dist']][:num_taps]
    closest_taps= closest_taps.reset_index()
    df1 = closest_taps.loc[closest_taps['dist']<= dist]
    return df1

def getlocation():
    df2 = df.copy()
    return df2["location"].unique().tolist()

def get_non_functional_waterbodies(lat, lng, dist, num_taps=10):
    df3 = df.copy()
    df3 = df3[df3['status'].str.contains('Non-', regex=False)]
    return df3

def get_subjective_quality_label():
    df_subjective_quality_label = df.copy()
    return df_subjective_quality_label.subjective_quality.unique()

def get_subjective_quality_value():
    df_subjective_quality_value = df.copy()
    return df_subjective_quality_value.groupby(['subjective_quality']).size().reset_index(name='counts')

def get_water_sources_label():
    df_water_sources_label = df.copy()
    return df_water_sources_label.water_source.unique()

def get_water_sources_value():
    df_water_sources_value = df.copy()
    return df_water_sources_value.groupby(['water_source']).size().reset_index(name='counts')