from turtle import title
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import streamlit as st
from water_recommendation_distance import closest_taps_distance, getlocation
import altair as alt
import geocoder
from geopy.geocoders import Nominatim
import plotly.express as px


st.set_page_config(layout="wide")
st.title("Explore Water Points in Nigeria")

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

state = 'Osun'

state1 = st.sidebar.selectbox("Select Your State of Interest: ", ("Abia", "Adamawa", \
      "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River",\
           "Delta", "Ebonyi", "Edo", "Enugu", "Ekiti", "Gombe", "Imo", "Jigawa", "Kaduna",\
                "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", \
               "Ogun", "Osun", "Ondo", "Plateau", "Rivers", "Sokoto", "Taraba", \
               "Yobe", "Zamfara"))



df = load_data(state1)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Status of Water in {}".format(state1))
    status = df['status'].value_counts()[:4]
    df_s = pd.DataFrame({"Frequency": status.values}, index = status.index)
    df_s['status'] = df_s.index
    fig = px.bar(df_s, y="Frequency", x="status", color="status", title="Status of Water in {}".format(state1))
    st.plotly_chart(fig)
    #st.bar_chart(df['status'].value_counts()[:4])

with col2:
    st.caption("Map of Water Points in {}".format(state1))
    st.map(df)

with col3:
    quality = df['subjective_quality'].value_counts()
    df_q = pd.DataFrame({"counts": quality.values}, index = quality.index)
    df_q.index.names = ["quality"]
    df_q['quality'] = df_q.index
    fig = px.pie(df_q, values='counts', names='quality', title = "The quality of Water in {}".format(state1))
    st.plotly_chart(fig)

#df_q.plot.pie(y = 'counts', figsize=(6,8))
dist = st.slider('Select a distance',0, 20, 8)
st.write("Distance: ", dist)

no_taps = st.slider('Select a Number of taps',0, 20, 8)
st.write("Number of taps: ", no_taps)

#Radio button to select location
loc = st.radio(
    "Select your prefered location",
    ('Current Location','{} Location'.format(state1),"Select"))

#Instantiating geolocator
geolocator = Nominatim(user_agent="app1")

if loc == "Current Location":
    g = geocoder.ip('me')
    latlng = g.latlng
    lat = latlng[0]
    lng = latlng[1]
elif loc == "{} Location".format(state1):
    #geolocator = Nominatim(user_agent="app1")
    location = geolocator.geocode(state1)
    lat = location.latitude
    lng = location.longitude
elif loc == "Select":
    selloc = st.selectbox(
     'How would you like to be contacted?',
     getlocation())
    location = geolocator.geocode(selloc)
    
    if location == None:
        location = geolocator.geocode(state1)
        lat = location.latitude
        lng = location.longitude
    else:
        lat = location.latitude
        lng = location.longitude
        # if lat and long are not in range constrain to default range of osun region
        if (float(lat) < float('7.060309')) or (float(lat) > float('8.061898')) or (float(lng) < float('4.032004')) or (float(lng) > float('5.055003')):
            location = geolocator.geocode(state1)
            lat = location.latitude
            lng = location.longitude

#display latitude and longitude
st.write("Latitude: {}, Longitude {}".format(lat, lng))

#Submit button to confirm distance, No of taps and Region
btn = st.button("Submit")

#find all the taps near by
taps = closest_taps_distance(df,lat,lng,dist, no_taps)

if btn:
    st.subheader("The {} Nearest Water Points Distances".format(no_taps))

    c = alt.Chart(taps).mark_bar().encode(
        x='location', y='dist',  color='location', tooltip=['location', 'population', 'dist'])

    st.altair_chart(c, use_container_width=True)
    
    #Display Data frame
    st.dataframe(taps)
