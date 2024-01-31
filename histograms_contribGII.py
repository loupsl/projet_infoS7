import pandas as pd
import plotly.express as px
import streamlit as st 

def plot_histo_GII():
    file_path = 'Updated_GII_with_Sorted_Clusters_and_All_Columns.csv'  
    data = pd.read_csv(file_path)

    categories = {
        'Reproductive Health': ['Maternal_mortality', 'Adolescent_birth_rate'],
        'Education': ['F_secondary_educ', 'M_secondary_educ'],
        'Economy': ['F_Labour_force', 'Seats_parliament', 'M_Labour_force']
    }

    category_averages = {category: [] for category in categories}

    for cluster in range(1, 6):
        cluster_data = data[data['Cluster'] == cluster]
        for category, columns in categories.items():
            category_average = cluster_data[columns].mean(axis=1).mean()
            category_averages[category].append(category_average)

    averages_df = pd.DataFrame(category_averages)
    averages_df['Cluster'] = range(1, 6)

    fig = px.bar(averages_df, 
                x='Cluster', 
                y=['Reproductive Health', 'Education', 'Economy'],
                title='Moyenne des Catégories par Cluster',
                labels={'value': 'Moyenne', 'variable': 'Catégorie'},
                color_discrete_sequence=px.colors.qualitative.Set1)


    fig.update_layout(barmode='stack', xaxis_title='Cluster', yaxis_title='Moyenne par Catégorie')

    st.plotly_chart(fig)
