import plotly.express as px
import streamlit as st
import pandas as pd 

plot_data_corrected = pd.read_csv('GDI_GII_country.csv')

countries_to_label = [
    "Yemen", "Afghanistan", "Niger", "Pakistan", "Chad", "Iraq",
    "Tajikistan", "Mali", "Lesotho", "Qatar", "Saudi Arabia",
    "United Arab Emirates", "Maldives", "Latvia", "Mongolia",
    "Panama", "Slovenia", "Bahrain", "Cuba", "Uzbekistan", "Lithuania", "Estonia", "Burundi",
    "Russian Federation", "Finland", "Sweden", "Danemark", "France", "Chile", "Argentina", "Colombia", "Congo",
    "Nigeria", "Liberia", "Malawi", "Madagascar", "Lebanon", "Morocco", "Indonesia", "Algeria", "Jordan",
    "Thailand", "Barbados", "India", "China", "Vietnam","Moldavia"
]

plot_data_corrected['Country_Label'] = plot_data_corrected['Country'].apply(
    lambda x: x if x in countries_to_label else None
)

fig = px.scatter(plot_data_corrected, 
                 x='GII', 
                 y='GDI_Value', 
                 text='Country_Label', 
                 title='Scatter plot of GDI vs. GII',
                 labels={'GII':'GII Value', 'GDI_Value':'GDI Value'})

fig.update_traces(textposition='top center')
fig.update_layout(showlegend=False, 
                  xaxis_title="GII Value", 
                  yaxis_title="GDI Value",
                  title_x=0.5, 
                  height=600, 
                  width=800)

st.plotly_chart(fig)


