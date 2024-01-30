import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import numpy as np 



def plot_prediction(gdi_melted, selected_country, p=5, d=1, q=0): 
    country_data = gdi_melted[gdi_melted['Country'] == selected_country]
    train_data = country_data['GDI'].dropna().astype(float)
    model = ARIMA(train_data, order=(p, d, q))
    model_fit = model.fit()
    last_year = country_data['Year'].values[-1]
    last_gdi_value = country_data['GDI'].iloc[-1]
    forecast_years = np.arange(last_year + 1, last_year + 11)
    forecast = model_fit.forecast(steps=10)
    forecast_values = np.insert(forecast.values, 0, last_gdi_value)
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
    fig.update_layout(hovermode='x',width=800,height=600)

    st.plotly_chart(fig)


