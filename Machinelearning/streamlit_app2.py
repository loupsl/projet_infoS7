import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from predictions import get_predictions_and_actual_gdi, get_available_countries

st.title('Analyse du Gender Development Index (GDI)')



available_countries = get_available_countries()
selected_country = st.selectbox('Choisissez un pays', available_countries)

if selected_country:
    predictions, actual_gdi = get_predictions_and_actual_gdi(selected_country)
    st.subheader(f'Résultats pour {selected_country}')

    
    mse_scores = predictions.pop('MSE', {})
    st.write("MSE Scores and Interpretations:")
    for method, mse in mse_scores.items():
        interpretation = "Bonne précision" if mse < 0.01 else "Précision modérée"
        st.write(f"{method}: MSE = {mse:.5f} - {interpretation}")

    
    fig, ax = plt.subplots()
    ax.plot(actual_gdi['Year'], actual_gdi['GDI'], 'k--', label='Données Réelles')

    for model, pred in predictions.items():
        ax.plot(np.arange(2022, 2041), pred, label=model)

    ax.set_xlabel('Année')
    ax.set_ylabel('GDI')
    ax.set_xticks(np.arange(1990, 2041, 5)) 
    ax.legend()
    st.pyplot(fig)
else:
    st.write("Veuillez sélectionner un pays pour afficher les résultats.")
