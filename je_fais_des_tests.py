import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.stats import pearsonr 
import plotly.express as px 



def create_histogram_for_countryGDI(df, country):
    def convert_to_numeric(column):
        return pd.to_numeric(column.str.replace(',', '').str.replace(' ', ''), errors='coerce')
    for col in df.columns.drop(['HDI Rank', 'Country']):
        df[col] = convert_to_numeric(df[col])
    df_transform = load_and_transform_data(df)
    data_pays = df_transform[df_transform['Country'] == country]
    data_pays_num = data_pays.select_dtypes(include='number').T
    data_pays_num.columns = ['Value']
    data_pays_num['Variable'] = data_pays_num.index
    fig = px.bar(data_pays_num, x='Variable', y='Value', title=f'Valeurs des Indicateurs pour {country}', 
                 width=800, height=600)
    fig.update_layout(yaxis_type="log")
    return fig

def create_histogram_for_countryGII(df, country):
    df_transform = load_and_transform_data(df) 
    data_pays = df_transform[df_transform['Country'] == country]
    data_pays_num = data_pays.select_dtypes(include='number').T.reset_index()
    data_pays_num.columns = ['Variable', 'Value']
    color_category_mapping = {
        'Maternal_mortality': ('red', 'Santé'),
        'Adolescent_birth_rate': ('red', 'Santé'),
        'F_secondary_educ': ('yellow', 'Education'),
        'M_secondary_educ': ('yellow', 'Education'),
        'F_Labour_force': ('green', 'Economie'),
        'M_Labour_force': ('green', 'Economie'),
        'Seats_parliament' : ('green','Economie'),
        'GII': ('blue', 'Données'),
        'Rank': ('blue', 'Données')
    }
    data_pays_num['Color'] = data_pays_num['Variable'].map(lambda x: color_category_mapping.get(x, ('gray', 'Autre'))[0])
    data_pays_num['Category'] = data_pays_num['Variable'].map(lambda x: color_category_mapping.get(x, ('gray', 'Autre'))[1])
    fig = px.bar(data_pays_num, x='Variable', y='Value', color='Category',
                 title=f'Histogramme pour {country}')

    fig.update_layout(xaxis_title='Variable', yaxis_title='Valeur', yaxis_type = "log")
    
    return fig


def load_and_transform_data(df):
    if df.iloc[0, 0] != df.iloc[0, 0]:  
        df = df.drop(0).reset_index(drop=True)
    df = df.replace(',', '', regex=True)
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

    return df


st.title('Histogramme des Indicateurs pour un Pays Sélectionné')


uploaded_file = st.file_uploader("Importez un fichier CSV", type=["csv"])
if uploaded_file is not None:
    file_name = uploaded_file.name 

    if file_name == "GDI_detail_2019.csv" : 
        df = pd.read_csv(uploaded_file,skiprows=[1]) 
        selected_country = st.selectbox('Choisissez un pays', df['Country'].unique())
        histogram_fig = create_histogram_for_countryGDI(df, selected_country)

    else: 
        df = pd.read_csv(uploaded_file) 
        selected_country = st.selectbox('Choisissez un pays', df['Country'].unique())
        histogram_fig = create_histogram_for_countryGII(df, selected_country)


    st.plotly_chart(histogram_fig)



        

