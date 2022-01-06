import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import streamlit as st
from water_recommendation import closest_taps
import altair as alt

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

taps = closest_taps(osun)

st.write(taps)

st.subheader("The Ten Nearest Water Points Distances")

#st.bar_chart(taps['dist'])


c = alt.Chart(taps).mark_bar().encode(
     x='location', y='dist',  color='location', tooltip=['location', 'population', 'dist'])

st.altair_chart(c, use_container_width=True)


st.subheader("The Ten Nearest Water Points With the population they serve")

d = alt.Chart(taps).mark_bar().encode(
     x='location', y='population',  color='location', tooltip=['location', 'population', 'dist'])

st.altair_chart(d, use_container_width=True)