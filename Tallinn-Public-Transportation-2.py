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
mapping = {2: 'Buss', 1: 'Troll', 3: 'Tramm'}
dataf['TransportType'] = dataf['TransportType'].map(mapping)

# Keep only meaningful columns
df = dataf[['TransportType', 'TransportLineNumber', 'Longitude', 'Latitude']]



# Report title
st.header('Tallinna ühistranspordi asukohad')


def load_data(nrows):
    data = df
    return data

data_load_state = st.text('Andmestik laeb...')
data = load_data(10000)
data_load_state.text("Andmestik laetud. Info andmestiku kohta: \nhttps://avaandmed.eesti.ee/datasets/uhistranspordivahendite-asukohad-reaalajas")


    
# create a multiselect for transport type
type_filter = st.multiselect(
    'Vali transporditüüp',
    data['TransportType'].unique()
)

if len(type_filter) == 0:
    type_filter = data['TransportType'].unique()
    

# create a multiselect for transport number

nodf = data[data['TransportType'].isin(type_filter)]

line_filter = st.multiselect(
    'Vali liini number',
    nodf['TransportLineNumber'].sort_values().unique()
)

if len(line_filter) == 0:
    line_filter = data['TransportLineNumber'].unique()


# Cretae map visual

filtereddata = data[data['TransportLineNumber'].isin(line_filter)&data['TransportType'].isin(type_filter)]

st.pydeck_chart(pdk.Deck(
    map_style=None,
     initial_view_state=pdk.ViewState(
        filtereddata['Longitude'].mean(),
        filtereddata['Latitude'].mean(),
        zoom=11,
        tooltip={
        "text": "TEXT",
        'style': {
            'backgroundColor': 'white',
            'color': 'blue'
        }
            }
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data[data['TransportLineNumber'].isin(line_filter)&data['TransportType'].isin(type_filter)],
            get_position='[Longitude, Latitude]',
            get_color='[0, 0, 255, 160]',
            get_radius=20,
             pickable=True,
            auto_highlight=True
        ),
    ],
))


# Selection for raw data
if st.checkbox('Näita algandmeid'):
    st.subheader('Algandmed')
    st.write(data)
