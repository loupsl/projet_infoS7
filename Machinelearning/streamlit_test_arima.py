import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

file_path = "C://Users/pelis/Documents/Mines2A/projet_infoS7/GDI_1990_2021.csv"
gdi_data = pd.read_csv(file_path)


st.title('Prédictions du Gender Development Index avec ARIMA')

gdi_melted = gdi_data.melt(id_vars=['ISO3', 'Country', 'Continent', 'Hemisphere', 'Human Development Groups', 'UNDP Developing Regions', 'HDI Rank (2021)'],
                           var_name='Year', value_name='GDI', 
                           value_vars=[col for col in gdi_data.columns if col.startswith('Gender Development Index')])
gdi_melted['Year'] = gdi_melted['Year'].str.extract('(\d+)').astype(int)
gdi_melted = gdi_melted.sort_values(by=['Country', 'Year'])

country_list = gdi_melted['Country'].unique()

selected_country = st.selectbox('Choisissez un pays', country_list)

if selected_country:

    country_data = gdi_melted[gdi_melted['Country'] == selected_country]
    
    train_data = country_data['GDI'].dropna().astype(float)

    
    model = ARIMA(train_data, order=(5,1,0))  # les paramètres p, d, q doivent être ajustés
    model_fit = model.fit()

    last_year = country_data['Year'].values[-1]
    last_gdi_value = country_data['GDI'].iloc[-1]

    forecast_years = np.arange(last_year, last_year + 10)
    forecast = model_fit.forecast(steps=10)

    forecast_values = np.insert(forecast.values, 0, last_gdi_value)

    fig, ax = plt.subplots()
    ax.plot(country_data['Year'], country_data['GDI'], label='Données Réelles')
    ax.plot([last_year, forecast_years[0]], [last_gdi_value, forecast_values[1]], 'o')
    ax.plot(forecast_years, forecast_values[1:], label='Prédictions ARIMA')
    ax.set_xlabel('Année')
    ax.set_ylabel('GDI')
    ax.set_xlim([1990, forecast_years[-1]])
    ax.legend()
    st.pyplot(fig)

