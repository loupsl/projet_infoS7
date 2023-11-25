import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("Gender_Inequality_Index.csv")

st.title("Création de profils de pays en fonction du GII")


variable_gii = df.columns[2]
variable_pays = df.columns[0]

# groupes en fonction du GII (ici on en prend 5)
num_groups = 5
df['GII Group'] = pd.qcut(df[variable_gii], num_groups, labels=False)

df['GII Group'].replace('nan', 'None', inplace=True)

df['GII Group'] = df['GII Group'].apply(lambda x: str(int(x) + 1) if not pd.isna(x) else 'None')


col1, col2 = st.columns(2)

# affichage du tableau en 2 colonnes 
col1.dataframe(df[[variable_pays, variable_gii, 'GII Group']].sort_values(by='GII Group').iloc[:len(df)//2])
col2.dataframe(df[[variable_pays, variable_gii, 'GII Group']].sort_values(by='GII Group').iloc[len(df)//2:])

#graphique illustrant les groupes
plt.figure(figsize=(20, 20))
sns.scatterplot(x=variable_gii, y=variable_pays, hue='GII Group', data=df[df['GII Group'] != 'None'], palette=f"viridis_r", legend='full')
plt.xlabel(variable_gii)
plt.ylabel(variable_pays)
plt.title(f"Groupes de pays en fonction de {variable_gii}")
st.pyplot()
