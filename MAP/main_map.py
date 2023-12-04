from create_map_GII import create_map_GII
from create_map_GDIyear import create_map_GDI
from create_map_gender import create_map_genderpassport
import folium
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd

st.title("Affichage des cartes")


selected_map = st.radio("Choisissez la carte du monde à afficher:", ["Gender Inequality Index (GII)","Gender Development Index (GDI) since 1990","Gender appliance for a passport since 2003"])


if selected_map == "Gender Inequality Index (GII)":

    st.title("Carte du Monde - Gender Inequality Index (GII)")
    df_gii = pd.read_csv("Gender_Inequality_Index.csv")
    folium_static(create_map_GII(df_gii))
    st.subheader("Gender Inequality Index")
    st.dataframe(df_gii)

elif selected_map == "Gender Development Index (GDI) since 1990":

    st.title("Carte du Monde - Gender Development Index (GDI)")

    selected_year = selected_year = st.slider("Sélectionnez une année", min_value=1990, max_value=2021, value=2021)

    df_gdi = pd.read_csv("GDI_1990_2021.csv")

    folium_static(create_map_GDI(df_gdi,selected_year))

    st.subheader(f"Les 5 pays les plus égalitaires en {selected_year}")
    top_egalitaires = df_gdi.sort_values(by=f'Gender Development Index ({selected_year})',ascending=False).head(5)
    st.dataframe(top_egalitaires)

    st.subheader(f"Les 5 pays les moins égalitaires en {selected_year}")
    top_inegalitaires = df_gdi.sort_values(by=f'Gender Development Index ({selected_year})').head(5)
    st.dataframe(top_inegalitaires)

elif selected_map == "Gender appliance for a passport since 2003":

    st.title("")
    df_passport = pd.read_csv("C:/Users/pelis/Documents/Mines2A/projet_infoS7/gender_apply_passeport/f4bc7e60-3002-4965-b634-58394c135c0c_Data.csv")
    selected_year = st.slider ("Sélectionner une année", 2003, 2022, value = 2022)
    folium_static(create_map_genderpassport(df_passport,selected_year))
