import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px 



def create_histogram_for_countryGDI(df,country):
    """ def load_and_transform_data(df):
        if df.iloc[0, 0] != df.iloc[0, 0]:  
            df = df.drop(0).reset_index(drop=True)
        df = df.replace(',', '', regex=True)
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass
        return df """
    df_transform = df
    data_pays = df_transform[df_transform['Country'] == country]
    data_pays_num = data_pays.select_dtypes(include='number').T.reset_index()
    data_pays_num.columns = ['Variable', 'Value']
    color_category_mapping = {
        'Lif_Expec_Female': ('red', 'Santé'),
        'Lif_Excep_Male': ('red', 'Santé'),
        'Excep_Yrs_Schooling_Female': ('yellow', 'Education'),
        'Excep_Yrs_Schooling_Male': ('yellow', 'Education'),
        'Mean_Yrs_Schooling_Female': ('yellow', 'Education'),
        'Mean_Yrs_Schooling_Male': ('yellow', 'Education'),
        'GNI_PC_Female': ('green', 'Economie'),
        'GNI_PC_Male': ('green', 'Economie'),
        'HDI Rank': ('blue', 'Données'),
        'GDI_Value': ('blue', 'Données'),
        'GDI_Group': ('blue', 'Données'),
        'HDI_Female': ('blue', 'Données'),
        'HDI_Male': ('blue', 'Données')
    }
    data_pays_num['Color'] = data_pays_num['Variable'].map(lambda x: color_category_mapping.get(x, ('gray', 'Autre'))[0])
    data_pays_num['Category'] = data_pays_num['Variable'].map(lambda x: color_category_mapping.get(x, ('gray', 'Autre'))[1])
    fig = px.bar(data_pays_num, x='Variable', y='Value', color='Category', title=f'Histogramme pour {country}',width=800, height=600)
    fig.update_layout(xaxis_title='Variable', yaxis_title='Valeur', yaxis_type = "log")
    return fig

def create_histogram_for_countryGII(df, country):
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
    fig = px.bar(data_pays_num, x='Variable', y='Value', color='Category', title=f'Histogramme pour {country}',width=800, height=600)
    fig.update_layout(xaxis_title='Variable', yaxis_title='Valeur', yaxis_type = "log")
    return fig





    



        

