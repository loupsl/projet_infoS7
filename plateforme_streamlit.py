import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.stats import pearsonr 


st.title("Importation de jeu de données avec Streamlit")

# Ajouter un bouton pour importer le jeu de données
uploaded_file = st.file_uploader("Importez un fichier CSV", type=["csv"])


if uploaded_file is not None:

    # Charger le jeu de données dans un DataFrame
    df = pd.read_csv(uploaded_file)

    st.dataframe(df.head(50))

    quantitative_cols = df.select_dtypes(include=["float64","int64"])

    selected_tab = st.radio("Sélectionnez l'onglet :", ("Informations et Résumé", "Nuage de Points","Histogramme","Comparer les statistiques entre groupes"))

   
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

        st.subheader("Matrice de corrélation")
        corr_matrix = quantitative_cols.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=.5)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

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
            st.success(f"Il y a une corrélation statistiquement significative entre {variable_a} et {variable_b}.")
        else:
            st.warning(f"Il n'y a pas de corrélation statistiquement significative entre {variable_a} et {variable_b}.")


    elif selected_tab == "Nuage de Points":
        
        st.header("Nuage de Points")

        variable_x = st.selectbox("Variable de l'axe des abscisses", df.columns)
        variable_y = st.selectbox("Variable de l'axe des ordonnées", df.columns)

        show_regression_line = st.checkbox("Droite de régression linéaire")

        # Afficher le nuage de points
        if st.button("Afficher le nuage de points"):
            fig, ax = plt.subplots()
            ax.scatter(df[variable_x], df[variable_y], color = "blue", label='Nuage de Points')

            if show_regression_line:
                if (df[variable_x].dtype == 'float64' or df[variable_x].dtype == 'int64') and (df[variable_y].dtype == 'float64' or df[variable_y].dtype == 'int64'):
                    sns.regplot(x=df[variable_x],y=df[variable_y], ax=ax, ci=None, color = "red", scatter=False, label='Droite de régression Linéaire')
                else: 
                    st.write("Les données ne sont pas de type numérique.")


            ax.set_xlabel(variable_x)
            ax.set_ylabel(variable_y)
            ax.set_title("Nuage de points")
            ax.legend()
            st.pyplot(fig)  


    elif selected_tab == "Histogramme":
        st.header("Histogramme")

        
        variable_histo = st.selectbox("Variable pour l'histogramme", quantitative_cols.columns)

        
        plt.figure(figsize=(8, 6))
        sns.histplot(data=df, x=variable_histo, kde=False, color='blue')
        plt.xlabel(variable_histo)
        plt.ylabel("Fréquence")
        plt.title(f"Histogramme de {variable_histo}")
        st.pyplot()
        
    elif selected_tab == "Comparer les statistiques entre groupes":

        st.header("Comparaison entre les groupes")

        







