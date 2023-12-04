import folium
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd

st.title("Test de l'affichage de la carte")


data = {
    'Country': ['France', 'Germany', 'Italy', 'Spain'],
    'Value': [25, 30, 15, 20]  # valeurs associées aux couleurs de la légende 
}
df = pd.DataFrame(data)

m = folium.Map(location=[0, 0], zoom_start=2)

# Ajout d'1 couche choroplèthe pour colorier les pays en fonction de la colonne 'Value'
folium.Choropleth(
    geo_data="https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json",
    name="choropleth",
    data=df,
    columns=['Country', 'Value'],
    key_on="feature.properties.name",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Values"
).add_to(m)


folium_static(m)
