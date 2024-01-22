#!/usr/bin/env python
# coding: utf-8

# In[7]:


import streamlit as st
import pandas as pd
import numpy as np
import io
import requests


# Get and format data
url = 'https://transport.tallinn.ee/gps.txt'
response = requests.get(url)
datatransport = response.text

# Convert the data to a dataframe
df = pd.read_csv(io.StringIO(datatransport))

# Add column names
df.columns = ['TransportType', 'TransportLineNumber', 'Longitude', 'Latitude', 'Column1', 'Column2', 'Column3', 'Column4']

# Add punctutation to Longitude and Latitude
df['Longitude'] = df['Longitude']/1000000
df['Latitude'] = df['Latitude']/1000000



@st.cache_data
def load_data(nrows):
    data = df
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done!")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Map of all transportation')
st.map(data)



