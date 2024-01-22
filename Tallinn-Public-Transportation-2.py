#!/usr/bin/env python
# coding: utf-8

# In[13]:


import streamlit as st
import pandas as pd
import numpy as np
import io
import requests
import pydeck as pdk


# Get and format data
url = 'https://transport.tallinn.ee/gps.txt'
response = requests.get(url)
datatransport = response.text

# Convert the data to a dataframe
dataf = pd.read_csv(io.StringIO(datatransport))

# Add column names
dataf.columns = ['TransportType', 'TransportLineNumber', 'Longitude', 'Latitude', 'Column1', 'Column2', 'Column3', 'Column4']

# Add punctutation to Longitude and Latitude
dataf['Longitude'] = dataf['Longitude']/1000000
dataf['Latitude'] = dataf['Latitude']/1000000

# map the values of column 'TransportType' to text values
mapping = {1: 'Buss', 2: 'Troll', 3: 'Tramm'}
dataf['TransportType'] = dataf['TransportType'].map(mapping)

# Keep only meaningful columns
df = dataf[['TransportType', 'TransportLineNumber', 'Longitude', 'Latitude']]





@st.cache_data
def load_data(nrows):
    data = df
    return data

data_load_state = st.text('Andmestik laeb...')
data = load_data(10000)
data_load_state.text("Andmestik laetud. Info andmestiku kohta: https://avaandmed.eesti.ee/datasets/uhistranspordivahendite-asukohad-reaalajas")


    
# create a multiselect for transport type
type_filter = st.multiselect(
    'Vali transporditüüp',
    data['TransportType'].unique()
)

# create a multiselect for transport number
type_filter = st.multiselect(
    'Vali liini number',
    data['TransportLineNumber'].unique()
)

st.subheader('Location of Public Transportation')
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=data,
            get_position='[longitude, latitude]',
            get_color='[0, 0, 255, 160]',
            get_radius=200,
             tooltip={
        'html':'TransportType: '+'TransportLineNumber',
        'style': {
            'backgroundColor': 'white',
            'color': 'blue'
        }
    }
        ),
    ],
))


# Selection for raw data
if st.checkbox('Näita algandmeid'):
    st.subheader('Algandmed')
    st.write(data)

