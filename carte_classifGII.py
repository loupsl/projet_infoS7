import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import json
from branca.element import Template, MacroElement

data_path = 'Gender_Inequality_Index_with_Clusters.csv'
data = pd.read_csv(data_path)
json_path = "fichiercree.json"
with open(json_path) as f:
    country_geo = json.load(f)

# Création d'une correspondance entre le nom du pays et son cluster
country_to_cluster = pd.Series(data.Cluster.values, index=data.Country).to_dict()

# Palette de couleurs pour les clusters
cluster_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Création d'un dictionnaire pour mapper les clusters aux couleurs
cluster_to_color = {i: cluster_colors[i] for i in range(len(cluster_colors))}

# Fonction pour retourner la couleur en fonction du nom du pays
def get_color_by_country(country):
    cluster = country_to_cluster.get(country, None)
    return cluster_colors[cluster] if cluster is not None else 'black'

# Création de la carte Folium avec une correspondance personnalisée
m = folium.Map(location=[20, 0], zoom_start=2)

# Boucle pour ajouter chaque pays avec sa couleur correspondante
for feature in country_geo['features']:
    country_name = feature['properties']['name']
    color = get_color_by_country(country_name)
    folium.GeoJson(
        feature,
        style_function=lambda feature, color=color: {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'dashArray': '5, 5',
            'fillOpacity': 0.7,
        }
    ).add_to(m)

# Création d'une légende HTML personnalisée
template = """
{% macro html(this, kwargs) %}

<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 150px; height: 130px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color: white;
            opacity: 0.8;">
    <p><b>Cluster Legend</b></p>
    <p><i style="background: #1f77b4"></i>Cluster 0</p>
    <p><i style="background: #ff7f0e"></i>Cluster 1</p>
    <p><i style="background: #2ca02c"></i>Cluster 2</p>
    <p><i style="background: #d62728"></i>Cluster 3</p>
    <p><i style="background: #9467bd"></i>Cluster 4</p>
</div>

{% endmacro %}
"""

# Ajout de la légende à la carte
macro = MacroElement()
macro._template = Template(template)
m.get_root().add_child(macro)

# Affichage de la carte dans Streamlit
folium_static(m)

