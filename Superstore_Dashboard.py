#!/usr/bin/env python
# coding: utf-8

# In[66]:


#Import necessary packages


import streamlit as st

import numpy as np
import pandas as pd
from millify import millify # shortens values (10_000 ---> 10k)
from streamlit_extras.metric_cards import style_metric_cards # beautify metric card with css
import plotly.graph_objects as go
import altair as alt 


# In[54]:


# Load data
df = pd.read_csv('Superstore 2023.csv')
df.head()


# In[55]:


# convert the dates column to datetime format
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y %H:%M:%S')


# In[56]:


# this function get the % change for any column by year and the specified aggregate
def get_per_year_change(col,df,metric):
    # Group by years and calculate the specified metric
    grp_years = df.groupby('Year')[col].agg([metric])[metric]
    # Calculate the % change
    grp_years = grp_years.pct_change() * 100
    grp_years.fillna(0, inplace=True)
    grp_years = grp_years.apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else 'NaN')

    return grp_years


# In[57]:


# Add new columns

# Extract the year and store it as a new column
df['Year'] = df['Order Date'].dt.year
# Calculate the difference between Shipped date and order date
df['Days to Ship'] = abs(df['Ship Date']- df['Order Date']).dt.days

# Calculate the % change of sales, profit and orders over the years
grp_years_sales = get_per_year_change('Sales',df,'sum')
grp_year_profit = get_per_year_change('Profit',df,'sum')
grp_year_orders = get_per_year_change('Order ID',df,'count')


# In[58]:


# Create metric card container

# creates the container for page title
dash_1 = st.container()

with dash_1:
    st.markdown("<h2 style='text-align: center;'>Superstore Sales Dashboard</h2>", unsafe_allow_html=True)
    st.write("")


# creates the container for metric card
dash_2 = st.container()

with dash_2:
    # get kpi metrics
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()

    col1, col2, col3 = st.columns(3)
    # create column span
    col1.metric(label="Sales", value= "$"+millify(total_sales, precision=2))
    
    col2.metric(label="Profit", value= "$"+millify(total_profit, precision=2))
    
    col3.metric(label="Orders", value=total_orders)
    
    # this is used to style the metric card
    style_metric_cards(border_left_color="#DBF227")


# In[59]:


# Create bar charts
# container for top 10 best selling and most profitable products
dash_3 = st.container()
with dash_3:
    
    # create columna for both graph
    col1,col2 = st.columns(2)
    # get the top 10 best selling products
    top_product_sales = df.groupby('Product Name')['Sales'].sum()
    top_product_sales = top_product_sales.nlargest(10)
    top_product_sales = pd.DataFrame(top_product_sales).reset_index()

    # get the top 10 most profitable products
    top_product_profit = df.groupby('Product Name')['Profit'].sum()
    top_product_profit = top_product_profit.nlargest(10)
    top_product_profit = pd.DataFrame(top_product_profit).reset_index()
   
    
    # create the altair chart
    with col1:
        chart = alt.Chart(top_product_sales).mark_bar(opacity=0.9,color="#9FC131").encode(
                x='sum(Sales):Q',
                y=alt.Y('Product Name:N', sort='-x')   
            )
        chart = chart.properties(title="Top 10 Selling Products" )

        
        st.altair_chart(chart,use_container_width=True)

    # create the altair chart
    with col2:
        chart = alt.Chart(top_product_profit).mark_bar(opacity=0.9,color="#9FC131").encode(
                x='sum(Profit):Q',
                y=alt.Y('Product Name:N', sort='-x')
                
            )
        chart = chart.properties(title="Top 10 Most Profitable Products" )

        st.altair_chart(chart,use_container_width=True)


# In[60]:


# container for avg shipping days and sales of different products categories over the years
dash_4 = st.container()
with dash_4:

    col1,col2 = st.columns([1,2])

    with col1:
        value =int(np.round(df['Days to Ship'].mean()))  # Example value

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': "Average Shipping Days"},
            gauge={'axis': {'range': [df['Days to Ship'].min() , df['Days to Ship'].max()]},
                'bar': {'color': "#005C53"},
                }
        ))

        fig.update_layout(height=350) 

        st.plotly_chart(fig, use_container_width=True)
  
    
    with col2:
        custom_colors = {'Furniture': '#005C53', 'Office Supplies': '#9FC131', 'Technology': '#042940'}


        bars = alt.Chart(df).mark_bar().encode(
            y=alt.Y('sum(Sales):Q', stack='zero', axis=alt.Axis(format='~s') ),
            x=alt.X('year:N'),
            #color=alt.Color('Category')
            color=alt.Color('Category:N', scale=alt.Scale(domain=list(custom_colors.keys()), range=list(custom_colors.values())))

        )

        text = alt.Chart(df).mark_text(dx=-15, dy=30, color='white').encode(
             y=alt.Y('sum(Sales):Q', stack='zero', axis=alt.Axis(format='~s') ),
            x=alt.X('year:N'),
            detail='Category:N',
            text=alt.Text('sum(Sales):Q', format='~s')
          )

        chart = bars + text

        chart = chart.properties(title="Sales trends for Product Categories over the years" )

        st.altair_chart(chart,use_container_width=True)


# In[ ]:




