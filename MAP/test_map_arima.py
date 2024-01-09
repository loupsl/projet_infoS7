import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import streamlit as st

# Charger les données GDI
gdi_data_path = "C://Users/pelis/Documents/Mines2A/projet_infoS7/GDI_1990_2021.csv"
gdi_data = pd.read_csv(gdi_data_path)

# Préparer les données pour ARIMA
gdi_melted = gdi_data.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='GDI', 
                           value_vars=[col for col in gdi_data.columns if col.startswith('Gender Development Index')])
gdi_melted['Year'] = gdi_melted['Year'].str.extract('(\d+)').astype(int)

# Créer un DataFrame pour les prédictions
predicted_gdi = pd.DataFrame(gdi_melted['Country'].unique(), columns=['Country'])

# Prédictions ARIMA pour chaque pays
for country in predicted_gdi['Country']:
    ts = gdi_melted[gdi_melted['Country'] == country]['GDI'].astype(float).dropna()
    if len(ts) >= 3:  # Assurez-vous d'avoir suffisamment de données pour le modèle ARIMA
        model = ARIMA(ts, order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=12)  # Prévoir jusqu'en 2032
        predicted_gdi.loc[predicted_gdi['Country'] == country, range(2022, 2033)] = forecast.values.reshape(1, -1)

# Fusionner les données réelles et les prédictions
full_gdi_data = pd.merge(gdi_data, predicted_gdi, on='Country', how='left')

# Vérifier la structure du DataFrame final
st.dataframe(full_gdi_data)
