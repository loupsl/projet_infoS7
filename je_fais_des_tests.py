import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.stats import pearsonr 
import plotly.express as px 


chemin_gdi = "C://Users/pelis/Documents/Mines2A/projet_infoS7\GDI_detail_2019.csv"
chemin_gii = "C://Users/pelis/Documents/Mines2A/projet_infoS7\Gender_Inequality_Index.csv"

# Fonction pour créer un histogramme pour un pays sélectionné
def create_histogram_for_country(df, country):
    # Filtrer les données pour le pays sélectionné
    data_pays = df[df['Country'] == country]

    # Supprimer les colonnes non numériques et transposer le DataFrame
    data_pays_num = data_pays.select_dtypes(include='number').T
    data_pays_num.columns = ['Value']
    data_pays_num['Variable'] = data_pays_num.index

    # Création de l'histogramme
    fig = px.bar(data_pays_num, x='Variable', y='Value', title=f'Valeurs des Indicateurs pour {country}')
    return fig

# Fonction pour charger les données et appliquer la transformation nécessaire
def load_and_transform_data(file_path):
    df = pd.read_csv(file_path)
    
    # Suppression de la première ligne si nécessaire (comme dans le cas de GDI)
    if df.iloc[0, 0] != df.iloc[0, 0]:  # Vérification si le premier élément est NaN
        df = df.drop(0).reset_index(drop=True)

    # Remplacer les virgules dans les nombres et convertir en float si nécessaire
    df = df.replace(',', '', regex=True)
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

    return df

# Chargement et transformation des données
df_gii = load_and_transform_data(chemin_gii)
df_gdi = load_and_transform_data(chemin_gdi)

# Exemple d'utilisation dans Streamlit
st.title('Histogramme des Indicateurs pour un Pays Sélectionné')

# Sélection du jeu de données
dataset = st.selectbox('Choisissez le jeu de données', ['GII', 'GDI'])

# Sélection du pays
if dataset == 'GII':
    selected_country = st.selectbox('Choisissez un pays', df_gii['Country'].unique())
    histogram_fig = create_histogram_for_country(df_gii, selected_country)
else:
    selected_country = st.selectbox('Choisissez un pays', df_gdi['Country'].unique())
    histogram_fig = create_histogram_for_country(df_gdi, selected_country)

# Afficher l'histogramme pour le pays sélectionné
st.plotly_chart(histogram_fig)



        

