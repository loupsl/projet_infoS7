
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
import matplotlib.pyplot as plt
import seaborn as sns

# Function to plot dendrogram
def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count
    linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)
    dendrogram(linkage_matrix, **kwargs)

# Load data
@st.cache
def load_data():
    data = pd.read_csv("Gender_Inequality_Index.csv")
    numerical_data = data.select_dtypes(include=[np.number])
    imputer = SimpleImputer(strategy='mean')
    numerical_data_imputed = imputer.fit_transform(numerical_data)
    scaler = StandardScaler()
    numerical_data_normalized = scaler.fit_transform(numerical_data_imputed)
    return data, numerical_data_normalized

# Main
def main():
    st.title('Ward Clustering of Countries based on Gender Inequality Index')
    data, numerical_data_normalized = load_data()
    
    # Ward Clustering
    ward_clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0, linkage='ward')
    ward_clustering.fit(numerical_data_normalized)

    # Creating linkage matrix for fcluster
    linkage_matrix = linkage(numerical_data_normalized, method='ward')

    # Determining a reasonable number of clusters
    distance_threshold = st.slider('Distance Threshold for Cluster Formation', min_value=0.0, max_value=10.0, value=1.5, step=0.1)
    labels = fcluster(linkage_matrix, distance_threshold, criterion='distance')

    # Plot Dendrogram
    st.subheader('Dendrogram')
    fig, ax = plt.subplots()
    plot_dendrogram(ward_clustering, truncate_mode='level', p=3, color_threshold=distance_threshold)
    st.pyplot(fig)

    # Creating a heatmap for cluster assignment
    st.subheader('Cluster Assignment Heatmap')
    cluster_map = pd.DataFrame({'Country': data['Country'], 'Cluster': labels})
    cluster_sorted = cluster_map.sort_values('Cluster')
    heatmap_data = pd.pivot_table(cluster_sorted, index='Country', columns='Cluster', aggfunc=len, fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(heatmap_data, ax=ax, cmap='viridis', cbar_kws={'label': 'Cluster'})
    st.pyplot(fig)

if __name__ == "__main__":
    main()
