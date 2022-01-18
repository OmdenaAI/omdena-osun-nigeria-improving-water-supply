from math import dist
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
import plotly.graph_objects as go



st.set_page_config(layout="wide")
st.image("image/logo.jpg", width=100)
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

@st.cache
def load():
    # Create an engine to connect to sqlite database
    engine = create_engine('sqlite:///water_points.db')
    conn = engine.connect()
    # Load the dataset from the database
    df = pd.read_sql_table('etlTable', con=conn)
    df = df.drop(['resident_latitude', 'resident_longitude', 'distance_in_km'], axis=1)
    return df

df_n = load()


with st.sidebar:
    state1 = st.selectbox("Select Your State of Interest: ", ("Abia", "Adamawa", \
      "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River",\
           "Delta", "Ebonyi", "Edo", "Enugu", "Ekiti", "Federal Capital Territory" , "Gombe", "Imo", "Jigawa", "Kaduna",\
                "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", \
               "Ogun", "Osun", "Ondo", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", \
               "Yobe", "Zamfara"))
    
    st.write('')
    st.write('')
    st.write("Total Number of Water Points in Nigeria is: {}".format(df_n.shape[0]))
    
    st.write('')
    st.write('')
    df = load_data(state1)
    st.write("{} state has {} Water Points".format(state1, df.shape[0]))

    st.write('')
    st.write('')
    url = "https://github.com/OmdenaAI/omdena-osun-nigeria-improving-water-supply"
    st.write("Check out the Project Github Repository @ [Omdena Osun Nigeria Improving Water Supply](%s)" % url)




df = load_data(state1)
col1, col2, col3 = st.columns(3)

with col1:
    status = df['status'].value_counts()[:4]
    df_s = pd.DataFrame({"Frequency": status.values}, index = status.index)
    df_s['status'] = df_s.index
    fig = px.bar(df_s, y="Frequency", x="status", color="status", title="Status of Water in {} state".format(state1))
    st.plotly_chart(fig)
    #st.bar_chart(df['status'].value_counts()[:4])

with col2:
    st.caption("Map of Water Points in {} state".format(state1))
    st.map(df)

with col3:
    quality = df['subjective_quality'].value_counts()
    df_q = pd.DataFrame({"counts": quality.values}, index = quality.index)
    df_q.index.names = ["quality"]
    df_q['quality'] = df_q.index
    fig = px.pie(df_q, values='counts', names='quality', title = "The quality of Water in {}".format(state1))
    st.plotly_chart(fig)

#df_q.plot.pie(y = 'counts', figsize=(6,8))


st.write("")
st.write("")
st.write("")
st.subheader("Select the Number of Nearby Water Points  You Want:")

st.write("")
st.write("")

dist = st.selectbox("Choose the max radius/distance of Nearby Water Points: ", 
 (2, 4, 6, 8, 10, 20, 30))

st.write("")
no_taps = st.selectbox("How Many Nearby Water Points do you want to View? ", (5, 10, 15))
st.write("")

#dist = st.slider('Select a distance',0, 20, 8)
#st.write("Distance: ", dist)
#no_taps = st.slider('Select a Number of taps',0, 20, 8)
#st.write("Number of taps: ", no_taps)

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
    st.subheader("The {} Nearest Water Points".format(no_taps))

    c = alt.Chart(taps).mark_bar().encode(
        x='location', y='dist',  color='location', tooltip=['location', 'population', 'dist'])

    #st.altair_chart(c, use_container_width=True)

    plot = go.Figure(data=[go.Bar(
    name = 'Population',
    x = taps['location'],
    y = taps['population']
    ),
                       go.Bar(
    name = 'Distance',
    x = taps['location'],
    y = taps['dist']*100
    )
    ])

    plot.update_layout(legend_title_text = "Location")
    plot.update_layout(title = "{} Nearby Water Points By Distance and Population they serve".format(no_taps))
    plot.update_xaxes(title_text="Locations")
    plot.update_yaxes(title_text="Population/Distance in metres")

    st.plotly_chart(plot)



    #Display Data frame
    st.dataframe(taps.reset_index())
