import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import json

def map_cluster_GII(data_path):
    data = pd.read_csv(data_path)
    json_path = "fichierGII.json"
    with open(json_path) as f:
        country_geo = json.load(f)

    country_to_cluster = pd.Series(data.Cluster.values, index=data.Country).to_dict()
    cluster_colors = ["#D4E6F1", "#A9CCE3", "#7FB3D5", "#5499C7", "#2980B9"]
    cluster_to_color = {i: cluster_colors[i] for i in range(len(cluster_colors))}
    def get_color_by_country(country):
        cluster = country_to_cluster.get(country, None)
        return cluster_colors[cluster-1] if cluster is not None else 'black'
    m = folium.Map(location=[20, 0], zoom_start=2)
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
                'legend_name' : 'Représentation des clusters',
            }
        ).add_to(m)
    folium_static(m)

def map_cluster_GDI(data_path):
    data = pd.read_csv(data_path)
    json_path = "fichierGDI.json"
    with open(json_path) as f:
        country_geo = json.load(f)

    country_to_cluster = pd.Series(data.Cluster.values, index=data.Country).to_dict()
    cluster_colors = ["#D4E6F1", "#A9CCE3", "#7FB3D5", "#5499C7", "#2980B9"]
    cluster_to_color = {i: cluster_colors[i] for i in range(len(cluster_colors))}
    def get_color_by_country(country):
        cluster = country_to_cluster.get(country, None)
        return cluster_colors[cluster-1] if cluster is not None else 'black'
    m = folium.Map(location=[20, 0], zoom_start=2)
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
                'legend_name' : 'Représentation des clusters',
            }
        ).add_to(m)
    folium_static(m)

