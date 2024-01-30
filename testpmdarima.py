import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pmdarima import auto_arima

def plot_prediction(gdi_melted, selected_country): 
    country_data = gdi_melted[gdi_melted['Country'] == selected_country]
    train_data = country_data['GDI'].dropna().astype(float)

    # Utilisation de auto_arima avec des paramètres ajustés
    model = auto_arima(train_data, start_p=0, start_q=0,
                       max_p=10, max_q=10, m=12,
                       seasonal=True,  # Activez si les données présentent une saisonnalité
                       d=None, trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    model_fit = model.fit(train_data)

    last_year = country_data['Year'].values[-1]
    last_gdi_value = country_data['GDI'].iloc[-1]

    forecast_years = np.arange(last_year + 1, last_year + 11)
    forecast = model_fit.predict(n_periods=10)

    forecast_values = np.insert(forecast, 0, last_gdi_value)

    real_data = country_data[['Year', 'GDI']]
    real_data['Type'] = 'Données Réelles'

    forecast_data = pd.DataFrame({
        'Year': forecast_years,
        'GDI': forecast_values[1:],
        'Type': 'Prédictions ARIMA'
    })

    plot_data = pd.concat([real_data, forecast_data])

    fig = px.line(plot_data, x='Year', y='GDI', color='Type',
                  labels={'GDI': 'Gender Development Index'},
                  title=f'GDI pour {selected_country} (Réel vs Prédictions ARIMA)')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(hovermode='x')

    st.plotly_chart(fig)


file_path = "C://Users/pelis/Documents/Mines2A/projet_infoS7/GDI_1990_2021.csv"
gdi_data = pd.read_csv(file_path)

st.title('Prédictions du Gender Development Index avec ARIMA')

gdi_melted = gdi_data.melt(id_vars=['ISO3', 'Country', 'Continent', 'Hemisphere', 'Human Development Groups', 'UNDP Developing Regions', 'HDI Rank (2021)'],
                        var_name='Year', value_name='GDI', 
                        value_vars=[col for col in gdi_data.columns if col.startswith('Gender Development Index')])
gdi_melted['Year'] = gdi_melted['Year'].str.extract('(\\d+)').astype(int)
gdi_melted = gdi_melted.sort_values(by=['Country', 'Year'])
country_list = gdi_melted['Country'].unique()

selected_country = st.selectbox('Choisissez un pays', country_list)
if selected_country:
    plot_prediction(gdi_melted,selected_country)