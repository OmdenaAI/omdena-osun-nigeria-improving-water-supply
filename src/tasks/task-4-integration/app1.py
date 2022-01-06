import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import streamlit as st
from water_recommendation_distance import closest_taps_distance, getlocation
import altair as alt
import geocoder
from geopy.geocoders import Nominatim

st.title("A Web App For Getting Water Points Recommendations in Osun State, Nigeria")

@st.cache
def load_data(state):
    # Create an engine to connect to sqlite database
    engine = create_engine('sqlite:///water_points.db')
    conn = engine.connect()
    # Load the dataset from the database
    df = pd.read_sql_table('etlTable', con=conn)
    # Get the data frame of the state
    df_state = df[df.state==state]
    
    return df_state

osun = load_data('Osun')

col1, col2 = st.columns(2)

dist = col1.slider('Select a distance',0, 30, 2)
st.write("Distance: ", dist)

no_taps = col2.slider('Select a Number of taps',0, 30, 2)
st.write("Number of taps: ", no_taps)

#Radio button to select location
loc = st.radio(
    "Select your prefered location",
    ('Current Location','Osun Centre Location',"Select"))

#Instantiating geolocator
geolocator = Nominatim(user_agent="app1")

if loc == "Current Location":
    g = geocoder.ip('me')
    latlng = g.latlng
    lat = latlng[0]
    lng = latlng[1]
elif loc == "Osun Centre Location":
    #geolocator = Nominatim(user_agent="app1")
    location = geolocator.geocode("OSUN")
    lat = location.latitude
    lng = location.longitude
elif loc == "Select":
    selloc = st.selectbox(
     'How would you like to be contacted?',
     getlocation())
    location = geolocator.geocode(selloc)
    
    if location == None:
        location = geolocator.geocode("OSUN")
        lat = location.latitude
        lng = location.longitude
    else:
        lat = location.latitude
        lng = location.longitude
        # if lat and long are not in range constrain to default range of osun region
        if (float(lat) < float('7.060309')) or (float(lat) > float('8.061898')) or (float(lng) < float('4.032004')) or (float(lng) > float('5.055003')):
            location = geolocator.geocode("OSUN")
            lat = location.latitude
            lng = location.longitude

#display latitude and longitude
st.write("Latitude: {}, Longitude {}".format(lat, lng))

#Submit button to confirm distance, No of taps and Region
btn = st.button("Submit")

#find all the taps near by
taps = closest_taps_distance(osun,lat,lng,dist, no_taps)

if btn:
    st.subheader("The Ten Nearest Water Points Distances")

    c = alt.Chart(taps).mark_bar().encode(
        x='location', y='dist',  color='location', tooltip=['location', 'population', 'dist'])

    st.altair_chart(c, use_container_width=True)
    
    #Display Data frame
    st.dataframe(taps)
