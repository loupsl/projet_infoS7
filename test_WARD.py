import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# Charger les données GDI
gdi_data = pd.read_csv("Gender_Inequality_Index.csv")

# Préparation des données pour le clustering
# Supposons que gdi_data est un DataFrame avec les pays en lignes et les années en colonnes
X = gdi_data.drop('Country', axis=1)  # Supprimer la colonne 'Country' si présente

# Normalisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Appliquer la classification de Ward
Z = linkage(X_scaled, method='ward')

# Afficher le dendrogramme
plt.figure(figsize=(10, 7))
dendrogram(Z, labels=gdi_data['Country'].values)
plt.title("Dendrogramme avec la méthode de Ward")
plt.xlabel('Pays')
plt.ylabel('Distance')
plt.show()
