import pandas as pd
from scipy.stats import pearsonr

fichier_csv = "Gender_Inequality_Index.csv"
df = pd.read_csv(fichier_csv)

df_cleaned = df[['GII', 'F_secondary_educ']].dropna()

correlation, p_value = pearsonr(df_cleaned['GII'], df_cleaned['F_secondary_educ'])

# Afficher les résultats de l'analyse de corrélation
print(f"Correlation entre GII et Taux d'education des femmes : {correlation}")
print(f"P-value : {p_value}")

# Interprétation des résultats
if p_value < 0.05:
    print("Il y a une correlation statistiquement significative entre le GII et le Taux d'education des femmes.")
else:
    print("Il n'y a pas de correlation statistiquement significative entre le GII et le Taux d'education des femmes.")


# Effectuer un test t indépendant
#t_statistic, p_value = ttest_ind(df['GII_Men'], df['GII_Women'])


