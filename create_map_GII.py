import folium
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd

def create_map_GII(df):
    
    #converter = coco.CountryConverter()
    #df['Country'] = df['Country'].apply(lambda x: converter.convert(x, to='ISO3'))
    
    #suppression des lignes où la valeur du GII est "None"
    df = df.dropna(subset=['GII'])

    m = folium.Map(location=[0, 0], zoom_start=2)

    
    folium.Choropleth(
    geo_data="C:/Users/pelis/Documents/Mines2A/projet_infoS7/MAP/fichiercree.json",
    name="choropleth",
    data=df,
    columns=['Country', 'GII'],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Gender Inequality Index (GII)"
    ).add_to(m)
    return m
    