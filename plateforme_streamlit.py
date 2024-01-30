import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.stats import pearsonr 
import plotly.express as px 
import plotly.figure_factory as ff
import numpy as np 
from histograms import create_histogram_for_countryGDI, create_histogram_for_countryGII
from create_map_GII import create_map_GII
from create_map_GDIyear import create_map_GDI
from pred_arima import plot_prediction  
from streamlit_folium import folium_static

st.title("Importation de jeu de données avec Streamlit")


uploaded_file = st.file_uploader("Importez un fichier CSV", type=["csv"])
chemin_gdi = "GDI_detail_2019.csv"
chemin_gii = "Gender_Inequality_Index.csv"
chemin_gdi1990 = "GDI_1990_2021.csv"

if uploaded_file is not None:

    file_name = uploaded_file.name 
    if file_name == "GDI_detail_2019.csv" : 
        df = pd.read_csv(uploaded_file,skiprows=[1])
        def convert_to_numeric(column):
            return pd.to_numeric(column.str.replace(',', '').str.replace(' ', ''), errors='coerce')
        for col in df.columns.drop(['HDI Rank', 'Country']):
            df[col] = convert_to_numeric(df[col])
    else: 
        df = pd.read_csv(uploaded_file) 

    quantitative_cols = df.select_dtypes(include=["float64","int64"])
    with st.sidebar:
        selected_tab = st.radio("Sélectionnez l'onglet :", 
                            ('Informations et Résumé', 'Corrélations', 
                             'Visualisation', 'Classification', 'Prédictions pour le GDI'))

   #####################################################################


    if selected_tab == "Informations et Résumé":

        st.header("Informations et Résumé")
        st.dataframe(df.head(70))
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
                xaxis=dict(side='bottom')  
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
                width=800,
                height=800,
                xaxis=dict(side='bottom')  # Place la légende horizontale en dessous de la matrice
            )
            st.header('Matrice de corrélation')
            st.plotly_chart(fig_gdi)
    


        st.subheader("P-value et corrélation")
        variable_a = st.selectbox("Variable 1", quantitative_cols.columns)
        variable_b = st.selectbox("Variable 2", quantitative_cols.columns)
        if st.button("Afficher l'analyse de corrélation"):
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


        if file_name == "GDI_detail_2019.csv" : 
            selected_country = st.selectbox('Choisissez un pays', df['Country'].unique()) 
            histogram_fig = create_histogram_for_countryGDI(df, selected_country)

        else:  
            selected_country = st.selectbox('Choisissez un pays', df['Country'].unique()) 
            histogram_fig = create_histogram_for_countryGII(df, selected_country)

        if st.button("Afficher l'histogramme"):
            st.plotly_chart(histogram_fig)

        st.header("Carte du monde")

        if file_name == "GDI_detail_2019.csv": 

            selected_year = st.slider("Sélectionnez une année", min_value=1990, max_value=2021, value=2010)
            df_gdi = pd.read_csv("GDI_1990_2021.csv")
            folium_static(create_map_GDI(df_gdi,selected_year))

            st.subheader(f"Les 5 pays les plus égalitaires en {selected_year}")
            top_egalitaires = df_gdi.sort_values(by=f'Gender Development Index ({selected_year})',ascending=False).head(5)
            st.dataframe(top_egalitaires)
            st.subheader(f"Les 5 pays les moins égalitaires en {selected_year}")
            top_inegalitaires = df_gdi.sort_values(by=f'Gender Development Index ({selected_year})').head(5)
            st.dataframe(top_inegalitaires)


        elif file_name == "Gender_Inequality_Index.csv": 
            df_gii = pd.read_csv("Gender_Inequality_Index.csv")
            folium_static(create_map_GII(df))



        
    elif selected_tab == "Classification":
        st.title("Classification")
        st.header('Création de profils de pays avec K-Means')

        if file_name == "Gender_Inequality_Index.csv":
            data = pd.read_csv('Gender_Inequality_Index_with_Clusters.csv')

            st.sidebar.title("Classification des Pays")
            selected_cluster = st.sidebar.selectbox("Sélectionnez un Cluster", sorted(data['Cluster'].unique()))
            st.write(f"Pays dans le Cluster {selected_cluster}:")
            st.write(data[data['Cluster'] == selected_cluster][['Country', 'GII','Cluster']])

            st.header('Visualisation des Inégalités de Genre par Pays')

            data['Cluster'] = data['Cluster'].astype('category')
            metric = st.selectbox('Choisissez une métrique à visualiser:', data.columns[2:-1]) # exclure 'Country', 'Human_development', et 'Cluster'
            custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'] # Bleu, Orange, Vert, Rouge, Violet
            fig = px.scatter(data, x=metric, y='GII', color='Cluster',
                            hover_data=['Country'], title=f'Distribution de {metric} vs GII par Cluster',
                            color_discrete_sequence=custom_colors) 
            st.plotly_chart(fig)

            cluster_data = data[data['Cluster'] == selected_cluster]
            numeric_columns = cluster_data.select_dtypes(include=['float64', 'int64'])
            cluster_stats = numeric_columns.mean()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### Statistiques Moyennes pour le Cluster {selected_cluster}")
                st.markdown(f"**GII moyen:** {cluster_stats['GII']:.3f}")
                st.markdown(f"**Rang moyen:** {cluster_stats['Rank']:.1f}")
                st.markdown(f"**Mortalité maternelle moyenne:** {cluster_stats['Maternal_mortality']:.1f}")
                st.markdown(f"**Taux moyen de naissance chez les adolescentes:** {cluster_stats['Adolescent_birth_rate']:.2f}")

            with col2:
                st.markdown("### Détails Additionnels")
                if 'Seats_parliament' in cluster_stats:
                    st.markdown(f"**Pourcentage moyen de femmes dans le parlement:** {cluster_stats['Seats_parliament']:.2f}%")
                if 'F_secondary_educ' in cluster_stats:
                    st.markdown(f"**Éducation secondaire (femmes) moyenne:** {cluster_stats['F_secondary_educ']:.2f}%")
                if 'M_secondary_educ' in cluster_stats:
                    st.markdown(f"**Éducation secondaire (hommes) moyenne:** {cluster_stats['M_secondary_educ']:.2f}%")
                if 'F_Labour_force' in cluster_stats:
                    st.markdown(f"**Participation moyenne des femmes dans la force de travail:** {cluster_stats['F_Labour_force']:.2f}%")
                if 'M_Labour_force' in cluster_stats:
                    st.markdown(f"**Participation moyenne des hommes dans la force de travail:** {cluster_stats['M_Labour_force']:.2f}%")

            #carte du monde avec les différents clusters 

        if file_name == "GDI_detail_2019.csv":

            data = pd.read_csv("GDI_detail_2019_with_Clusters.csv")
            st.sidebar.title("Classification des Pays")
            selected_cluster = st.sidebar.selectbox("Sélectionnez un Cluster", sorted(data['Cluster'].unique()))
            st.write(f"Pays dans le Cluster {selected_cluster}:")
            st.write(data[data['Cluster'] == selected_cluster][['Country', 'GDI_Value', 'Cluster']]) # Remplacer 'GII' par 'GDI_Value'

            st.header('Visualisation des Inégalités de Genre par Pays')
            data['Cluster'] = data['Cluster'].astype('category')
            metric = st.selectbox('Choisissez une métrique à visualiser:', data.columns[2:-1]) # Exclure 'Country' et 'Cluster'
            custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'] # Bleu, Orange, Vert, Rouge, Violet
            fig = px.scatter(data, x=metric, y='GDI_Value', color='Cluster',
                            hover_data=['Country'], title=f'Distribution de {metric} vs GDI_Value par Cluster',
                            color_discrete_sequence=custom_colors)
            st.plotly_chart(fig)

            cluster_data = data[data['Cluster'] == selected_cluster]
            numeric_columns = cluster_data.select_dtypes(include=['float64', 'int64'])
            cluster_stats = numeric_columns.mean()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### Statistiques Moyennes pour le Cluster {selected_cluster}")
                st.markdown(f"**Valeur GDI moyenne:** {cluster_stats['GDI_Value']:.3f}")
                st.markdown(f"**IDH moyen pour les femmes:** {cluster_stats['HDI_Female']:.3f}")
                st.markdown(f"**IDH moyen pour les hommes:** {cluster_stats['HDI_Male']:.3f}")
            with col2:
                st.markdown("### Détails Additionnels")
                if 'Lif_Expec_Female' in cluster_stats:
                    st.markdown(f"**Espérance de vie moyenne des femmes:** {cluster_stats['Lif_Expec_Female']:.1f} ans")
                if 'Lif_Excep_Male' in cluster_stats:
                    st.markdown(f"**Espérance de vie moyenne des hommes:** {cluster_stats['Lif_Excep_Male']:.1f} ans")


    elif selected_tab == "Prédictions pour le GDI":
        gdi_data = pd.read_csv("GDI_1990_2021.csv")

        st.title('Prédictions du Gender Development Index avec ARIMA')

        gdi_melted = gdi_data.melt(id_vars=['ISO3', 'Country', 'Continent', 'Hemisphere', 'Human Development Groups', 'UNDP Developing Regions', 'HDI Rank (2021)'],
                                var_name='Year', value_name='GDI', 
                                value_vars=[col for col in gdi_data.columns if col.startswith('Gender Development Index')])
        gdi_melted['Year'] = gdi_melted['Year'].str.extract('(\\d+)').astype(int)
        gdi_melted = gdi_melted.sort_values(by=['Country', 'Year'])
        country_list = gdi_melted['Country'].unique()


        selected_country = st.selectbox('Choisissez un pays', country_list)

        p = st.slider('Choisir p (Auto-régression)', min_value=0, max_value=10, value=5)
        d = st.slider('Choisir d (Différenciation)', min_value=0, max_value=3, value=1)
        q = st.slider('Choisir q (Moyenne mobile)', min_value=0, max_value=10, value=0)

        if st.button('Afficher les prédictions'):
            plot_prediction(gdi_melted, selected_country, p, d, q)








