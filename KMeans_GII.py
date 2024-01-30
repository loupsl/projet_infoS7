import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'Gender_Inequality_Index.csv'
gender_data = pd.read_csv(file_path)
imputer = SimpleImputer(strategy='mean')
gender_data_imputed = imputer.fit_transform(gender_data.select_dtypes(include=['float64', 'int64']))
scaler = StandardScaler()
gender_data_scaled = scaler.fit_transform(gender_data_imputed)
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(gender_data_scaled)
gender_data['Cluster'] = clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=gender_data, x="GII", y="Maternal_mortality", hue="Cluster", palette="deep")
plt.title("Visualisation des Clusters Basée sur le GII et la Mortalité Maternelle")
plt.show()
