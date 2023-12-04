import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
from streamlit_folium import folium_static


def create_map_genderpassport(df,selected_year):

    data_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    gdf = gpd.read_file(data_url)

    variable_name = "A woman can apply for a passport in the same way as a man (1=yes; 0=no)" 
    filtered_data = df[df["Series Name"] == variable_name][["Country Name", f"{selected_year} [YR{selected_year}]"]]
    filtered_data[f"{selected_year} [YR{selected_year}]"] = pd.to_numeric(filtered_data[f"{selected_year} [YR{selected_year}]"], errors="coerce")

    # Fusionner les données GeoJSON avec les données filtrées
    merged_data = gdf.merge(filtered_data, left_on="name", right_on="Country Name")

    m = folium.Map(location=[0, 0], zoom_start=2)

    folium.Choropleth(
        geo_data=merged_data,
        name='choropleth',
        data=filtered_data,
        columns=['Country Name', f'{selected_year} [YR{selected_year}]'],
        key_on='feature.properties.name',
        fill_color='RdYlGn',  # Rouge pour 0, Vert pour 1
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'{variable_name} ({selected_year})'
    ).add_to(m)

    return m

