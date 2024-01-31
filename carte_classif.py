import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import json
import plotly.graph_objs as go 

def map_cluster_GII(data_path):
    data = pd.read_csv(data_path)
    json_path = "fichierGII.json"
    with open(json_path) as f:
        country_geo = json.load(f)

    country_to_cluster = pd.Series(data.Cluster.values, index=data.Country).to_dict()
    cluster_colors = ["#D6EAF8", "#AED6F1", "#5DADE2", "#2E86C1", "#1B4F72"]
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
    cluster_colors =["#D6EAF8", "#AED6F1", "#5DADE2", "#2E86C1", "#1B4F72"]

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

def plot_legend(): 
    blue_palette = ["#D6EAF8", "#AED6F1", "#5DADE2", "#2E86C1", "#1B4F72"]

    legend = go.Figure(data=[go.Bar(
        x=[1, 2, 3, 4, 5],
        y=[1, 1, 1, 1, 1],
        marker_color=blue_palette,
        marker_line_color=blue_palette,
        marker_line_width=1, 
        width=[0.5]*5  
    )])
    legend.update_layout(
        xaxis=dict(
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5'],
            tickmode='array',
            showgrid=False,
            showticklabels=True,
            tickfont=dict(size=10),
            range=[0.5, 5.5]
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            showline=False,
            zeroline=False
        ),
        barmode='overlay',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=20, b=20), 
        height=50,  # adjust height 
        width=400  
    )
    legend.update_layout(showlegend=False)

    st.plotly_chart(legend)
