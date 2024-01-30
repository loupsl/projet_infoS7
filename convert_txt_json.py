import json

# Chemin du fichier txt original
chemin_txt = 'C:/Users/pelis/Documents/Mines2A/projet_infoS7/MAP/fichiercreeGDI.txt'

# Chemin du nouveau fichier JSON
chemin_json = 'C:/Users/pelis/Documents/Mines2A/projet_infoS7/MAP/fichiercreeGDI.json'

# Lire le contenu du fichier txt
with open(chemin_txt, 'r') as fichier_txt:
    contenu_json = fichier_txt.read()

# Assurer que le contenu est un JSON valide
try:
    donnees = json.loads(contenu_json)
except json.JSONDecodeError:
    print("Le contenu du fichier txt n'est pas un JSON valide.")
    # Gérer l'exception ou arrêter l'exécution

# Écrire le contenu dans un nouveau fichier JSON
with open(chemin_json, 'w') as fichier_json:
    json.dump(donnees, fichier_json, indent=4)
