#import pandas as pd
#import numpy as np
#from sqlalchemy import create_engine
#import pydeck as pdk
import streamlit as st
from water_recommendation_distance import *
import altair as alt
import geocoder
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Water Sustainability Dashboard for Osun Region",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Get Water Points Recommendations in Osun State",anchor=False)

# @st.cache
# def load_data(state):
#     # Create an engine to connect to sqlite database
#     engine = create_engine('sqlite:///water_points.db')
#     conn = engine.connect()
#     # Load the dataset from the database
#     df = pd.read_sql_table('etlTable', con=conn)
#     # Get the data frame of the state
#     df_state = df[df.state==state]
    
#     return df_state

#osun = load_data('Osun')

col1, col2 = st.columns(2)

dist = col1.slider('Select a distance',0, 30, 2)
#st.write("Distance: ", dist)
col1.markdown("Distance: " + str(dist))

no_taps = col2.slider('Select a Number of taps',0, 30, 2)
#st.write("Number of taps: ", no_taps)
col2.markdown("Number of taps: " + str(no_taps))
    
#Radio button to select location
loc = col1.radio(
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
col1.write("Latitude: {}, Longitude {}".format(lat, lng))

#Submit button to confirm distance, No of taps and Region
btn = col1.button("Submit")

#find all the taps near by
taps = closest_taps_distance(lat,lng,dist, no_taps)
#find the non-functional water bodies
non_functional_waterbodies = get_non_functional_waterbodies(lat,lng,dist, no_taps)
#find the subjective_quality labels
lst_subjective_quality_label = get_subjective_quality_label()
#find the subjective_quality values
lst_subjective_quality_value = get_subjective_quality_value()
#find the water_sources labels
lst_water_sources_label = get_water_sources_label()
#find the water_sources values
lst_water_sources_value = get_water_sources_value()

#Print Metric of Total Population in selected area 
col2.metric("Total Population in the selected area", str(taps.population.sum()))

#Print Metric of Total Number of Functional Water Bodies in selected area 
col2.metric("Total Number of Functional Water Bodies in the selected area", str(len(taps)))

#Print Metric of Total Number of Non-Functional Water Bodies 
col2.metric("Total Number of Non-Functional Water Bodies", str(len(non_functional_waterbodies)))

labels_ws = lst_water_sources_label #'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes_ws = lst_water_sources_value.iloc[:,1] #[15, 30, 45, 10]
#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, ax1 = plt.subplots()
ax1.pie(sizes_ws,  labels=labels_ws, autopct='%1.1f%%',shadow=False, startangle=55)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
col1.text("")
col1.text("")
col1.text("")
col1.pyplot(fig1)
col1.text("Water Sources")
col1.table(lst_water_sources_value)

labels_sq = lst_subjective_quality_label #'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes_sq = lst_subjective_quality_value.iloc[:,1] #[15, 30, 45, 10]
#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig2, ax2 = plt.subplots()
ax2.pie(sizes_sq,  labels=labels_sq, autopct='%1.1f%%',shadow=False, startangle=55)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
col2.pyplot(fig2)
col2.text("")
col2.text("")
col2.text("Water Subjective Quality")
col2.table(lst_subjective_quality_value)

if btn:
    
    st.subheader("The " +  str(no_taps) + " Nearest Water Points Distances")

    c = alt.Chart(taps).mark_bar().encode(
        x='location', y='dist',  color='location', tooltip=['location', 'population', 'dist'])

    st.altair_chart(c, use_container_width=True)
    
    #Display Data frame
    st.table(taps)
    
    #df1 = pd.DataFrame({'lat':[lat],'lon': [lng]})

    #st.map(df1,zoom=16, use_container_width=True)
    
    # st.pydeck_chart(pdk.Deck(
    #  map_style='mapbox://styles/mapbox/light-v9',
    #  initial_view_state=pdk.ViewState(
    #      latitude=lat,
    #      longitude=lng,
    #      zoom=16,
    #      pitch=50,
    #  ),
    #  layers=[
    #      pdk.Layer(
    #         'HexagonLayer',
    #         data=df1,
    #         get_position='[lat, lon]',
    #         radius=dist,
    #         elevation_scale=4,
    #         elevation_range=[0, 1000],
    #         pickable=True,
    #         extruded=True,
    #      ),
    #      pdk.Layer(
    #          'ScatterplotLayer',
    #          data=df1,
    #          get_position='[lat, lon]',
    #          get_color='[200, 30, 0, 160]',
    #          get_radius=dist,
    #      ),
    #  ],
    # ))
    
    # col1, col2, col3, col4 = st.columns(4)
    # col1.metric("Total Population in the selected area", str(taps.population.sum()))
    # col2.metric("Total Number of Functional Water Bodies", str(len(taps)))
    # #col3.metric("Humidity", "86%", "4%")