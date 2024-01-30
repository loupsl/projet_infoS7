import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import streamlit as st

gdi_data_path = "C://Users/pelis/Documents/Mines2A/projet_infoS7/GDI_1990_2021.csv"
gdi_data = pd.read_csv(gdi_data_path)

gdi_melted = gdi_data.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='GDI', 
                           value_vars=[col for col in gdi_data.columns if col.startswith('Gender Development Index')])
gdi_melted['Year'] = gdi_melted['Year'].str.extract('(\d+)').astype(int)

predicted_gdi = pd.DataFrame(gdi_melted['Country'].unique(), columns=['Country'])


