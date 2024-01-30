import folium
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import country_converter as coco
from statsmodels.tsa.arima.model import ARIMA
import numpy as np 

def predict_GDI(gdi_data):

    gdi_melted = gdi_data.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='GDI',
                                value_vars=[col for col in gdi_data.columns if col.startswith('Gender Development Index')])
    gdi_melted['Year'] = gdi_melted['Year'].str.extract('(\d+)').astype(int)
    gdi_melted = gdi_melted.sort_values(by=['Country', 'Year'])

    predicted_gdi = pd.DataFrame(gdi_melted['Country'].unique(), columns=['Country'])
    for year in range(2022, 2032):
        predicted_gdi[str(year)] = np.nan  # ajouter les colonnes pour les années de prédiction

    
    for country in predicted_gdi['Country']:
        ts = gdi_melted[gdi_melted['Country'] == country]['GDI'].astype(float).dropna()
        if len(ts) >= 3:  
            model = ARIMA(ts, order=(5, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=10)
            predicted_gdi.loc[predicted_gdi['Country'] == country, [str(year) for year in range(2022, 2032)]] = forecast

    return predicted_gdi

    #country_list = gdi_melted['Country'].unique()

    #for country in country_list : 




def create_map_GDI(df_gdi, selected_year):

    if selected_year <= 2021: 
        selected_gdi_column = f"Gender Development Index ({selected_year})"
        df_selected_year = df_gdi[['Country', selected_gdi_column]]

    elif selected_year > 2021: 
        predicted_gdi = predict_GDI(df_gdi) 
        selected_gdi_column = selected_year
        df_selected_year = predicted_gdi[['Country',selected_gdi_column]]


    m = folium.Map(location=[0, 0], zoom_start=2)
    folium.Choropleth(
        geo_data="C:/Users/pelis/Documents/Mines2A/projet_infoS7/MAP/fichiercreeGDI.json",
        data=df_selected_year,
        columns=['Country', selected_gdi_column],
        key_on='feature.properties.name',
        fill_color='YlOrRd_r',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Gender Development Index ({selected_year})'
    ).add_to(m)

    return m
    


