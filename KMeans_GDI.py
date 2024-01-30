from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 

file_path = 'GDI_detail_2019.csv'
gdi_data = pd.read_csv(file_path, skiprows=[1])
imputer = SimpleImputer(strategy='mean')
gdi_data_imputed = imputer.fit_transform(gdi_data.select_dtypes(include=['float64', 'int64']))

scaler = StandardScaler()
gdi_data_scaled = scaler.fit_transform(gdi_data_imputed)
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(gdi_data_scaled)
gdi_data['Cluster'] = clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=gdi_data, x="HDI_Female", y="GDI_Value", hue="Cluster", palette="deep")
plt.title("Visualisation des Clusters Basée sur l'IDH des Femmes et la Valeur GDI")
plt.show()
