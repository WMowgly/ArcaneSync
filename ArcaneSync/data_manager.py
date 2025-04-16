import json
import os

# Le chemin du fichier JSON où sont stockées les données
data_file = "data.json"

# Charger les données depuis le fichier JSON
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Vérification si la clé 'joueurs' existe, sinon on l'initialise
        if "joueurs" not in data:
            data["joueurs"] = []  # On initialise la clé 'joueurs' vide si elle n'existe pas

        # Vérification que chaque joueur possède les clés 'hp' et 'mana'
        for joueur in data["joueurs"]:
            if "hp" not in joueur:
                joueur["hp"] = 100  # Valeur par défaut pour 'hp'
            if "mana" not in joueur:
                joueur["mana"] = 50  # Valeur par défaut pour 'mana'
        
        save_data(data)  # Sauvegarde les modifications
    else:
        # Si le fichier n'existe pas, créer un fichier avec une structure de base
        data = {"joueurs": [{"nom": "Joueur1", "hp": 100, "mana": 50}, {"nom": "Joueur2", "hp": 100, "mana": 50}]}
        save_data(data)
    
    return data

# Sauvegarder les données dans le fichier JSON
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)