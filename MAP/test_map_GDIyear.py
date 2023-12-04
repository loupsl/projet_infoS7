import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

df_gdi = pd.read_csv("GDI_1990_2021.csv")
st.title("Carte du Monde - Gender Development Index (GDI)")

selected_year = st.slider("Sélectionnez une année", min_value=1990, max_value=2021, value=2021)


selected_gdi_column = f"Gender Development Index ({selected_year})"
df_selected_year = df_gdi[['Country', selected_gdi_column]]

m = folium.Map(location=[0, 0], zoom_start=2)

folium.Choropleth(
    geo_data="https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json",
    data=df_selected_year,
    columns=['Country', selected_gdi_column],
    key_on='feature.properties.name',
    fill_color='YlOrRd_r',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f'Gender Development Index ({selected_year})'
).add_to(m)

folium_static(m)

st.subheader(f"Les 5 pays les plus égalitaires en {selected_year}")
top_egalitaires = df_gdi.sort_values(by=f'Gender Development Index ({selected_year})',ascending=False).head(5)
st.dataframe(top_egalitaires)

st.subheader(f"Les 5 pays les moins égalitaires en {selected_year}")
top_inegalitaires = df_gdi.sort_values(by=f'Gender Development Index ({selected_year})').head(5)
st.dataframe(top_inegalitaires)