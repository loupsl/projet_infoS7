import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.stats import pearsonr 
import plotly.express as px 
import plotly.figure_factory as ff
import numpy as np 

st.title("Importation de jeu de données avec Streamlit")

# Ajouter un bouton pour importer le jeu de données
uploaded_file = st.file_uploader("Importez un fichier CSV", type=["csv"])


if uploaded_file is not None:
    file_name = uploaded_file.name 
    # Charger le jeu de données dans un DataFrame
    df = pd.read_csv(uploaded_file)

    st.dataframe(df.head(50))

    quantitative_cols = df.select_dtypes(include=["float64","int64"])

    selected_tab = st.radio("Sélectionnez l'onglet :", ("Informations et Résumé", "Corrélations","Visualisation","Classification","Prédictions"))

   
    if selected_tab == "Informations et Résumé":
        st.header("Informations et Résumé")
        st.subheader("Statistiques sur les variables quantitatives")

        stats_data = []
        for col in quantitative_cols.columns:
            stats_data.append({
                "Variable": col,
                "Min": quantitative_cols[col].min(),
                "Max": quantitative_cols[col].max(),
                "Moyenne": quantitative_cols[col].mean()
            })

        stats_df = pd.DataFrame(stats_data)
        st.write(stats_df)

    elif selected_tab == "Corrélations":
        
        st.subheader("Matrice de corrélation")
        chemin_gdi = "C://Users/pelis/Documents/Mines2A/projet_infoS7\GDI_detail_2019.csv"
        chemin_gii = "C://Users/pelis/Documents/Mines2A/projet_infoS7\Gender_Inequality_Index.csv"

    
        def convert_to_numeric(column):
            return pd.to_numeric(column.astype(str).str.replace(',', ''), errors='coerce')
        

        if file_name == "Gender_Inequality_Index.csv": 
            gender_inequality_index_df = pd.read_csv(chemin_gii)
            numeric_columns_gii = gender_inequality_index_df.select_dtypes(include=[np.number])
            corr_matrix_gii = numeric_columns_gii.corr()
            fig_gii = ff.create_annotated_heatmap(
                z=corr_matrix_gii.to_numpy(),
                x=corr_matrix_gii.columns.tolist(),
                y=corr_matrix_gii.columns.tolist(),
                annotation_text=np.around(corr_matrix_gii.values, 2),
                colorscale='Viridis',
                showscale=True
            )
            fig_gii.update_layout(
                title='Gender Inequality Index Correlation Matrix',
                width=600,
                height=600,
                xaxis=dict(side='bottom')  # Place la légende horizontale en dessous de la matrice
            )
            st.header('Gender Inequality Index')
            st.plotly_chart(fig_gii)

        if file_name == "GDI_detail_2019.csv": 
            gdi_detail_2019_df = pd.read_csv(chemin_gdi)
            gdi_detail_2019_df = gdi_detail_2019_df.drop(0)
            gdi_columns_to_convert = ['GDI_Value', 'HDI_Female', 'HDI_Male', 'Lif_Expec_Female', 'Lif_Excep_Male',
                                    'Excep_Yrs_Schooling_Female', 'Excep_Yrs_Schooling_Male',
                                    'Mean_Yrs_Schooling_Female', 'Mean_Yrs_Schooling_Male',
                                    'GNI_PC_Female', 'GNI_PC_Male']

            for column in gdi_columns_to_convert:
                gdi_detail_2019_df[column] = convert_to_numeric(gdi_detail_2019_df[column])
            
            numeric_columns_gdi = gdi_detail_2019_df.select_dtypes(include=[np.number])
            corr_matrix_gdi = numeric_columns_gdi.corr()
            fig_gdi = ff.create_annotated_heatmap(
                z=corr_matrix_gdi.to_numpy(),
                x=corr_matrix_gdi.columns.tolist(),
                y=corr_matrix_gdi.columns.tolist(),
                annotation_text=np.around(corr_matrix_gdi.values, 2),
                colorscale='Viridis',
                showscale=True
            )
            fig_gdi.update_layout(
                title='GDI Detail 2019 Correlation Matrix',
                width=800,
                height=800,
                xaxis=dict(side='bottom')  # Place la légende horizontale en dessous de la matrice
            )

            st.header('Matrice de corrélation')
            st.plotly_chart(fig_gdi)
    


        st.subheader("P-value et corrélation")

        variable_a = st.selectbox("Variable 1", quantitative_cols.columns)
        variable_b = st.selectbox("Variable 2", quantitative_cols.columns)

        df_cleaned = df[[variable_a, variable_b]].apply(pd.to_numeric, errors='coerce').dropna()
        correlation, p_value = pearsonr(df_cleaned[variable_a], df_cleaned[variable_b])

        st.subheader("Résultats de l'analyse de corrélation")
        st.write(f"**Corrélation entre {variable_a} et {variable_b}:** {correlation:.4f}")
        st.write(f"**P-value :** {p_value}")

        # Interprétation des résultats
        if p_value < 0.05:
            st.success(f"Il y a une corrélation statistiquement significative (positive) entre {variable_a} et {variable_b}.")
        
        else:
            st.warning(f"Il n'y a pas de corrélation statistiquement significative entre {variable_a} et {variable_b}.")


    elif selected_tab == "Visualisation":
        
        st.header("Nuage de Points")

        variable_x = st.selectbox("Variable de l'axe des abscisses", df.columns)
        variable_y = st.selectbox("Variable de l'axe des ordonnées", df.columns)

        # affichage du nuage de points
        if st.button("Afficher le nuage de points"):
            df['Country'] = df['Country'].astype('category')

            fig = px.scatter(df, variable_x, variable_y, title='Nuage de points des valeurs par pays')

            if variable_x == "GDI_Value":
                maxvalue,minvalue = 1.1,0.3
            else:
                maxvalue,minvalue=1,0

            fig.update_xaxes(showticklabels=False) 
            fig.update_layout(
                yaxis=dict(range=[minvalue, maxvalue]),  
                xaxis=dict(categoryorder='total descending', tickangle=-45),
                width = 800,
                height = 600,
            )

            st.plotly_chart(fig)

        st.header("Histogramme")

        country = st.selectbox("Choisir un pays", df['Country'].unique())
        country_data = df[df['Country'] == country]
        #............................
        


        
    elif selected_tab == "Classification":

        st.header("Classification")



    elif selected_tab == "Prédictions":

        st.header("Prédictions")

        







