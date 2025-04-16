from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from data_manager import load_data, save_data  # Assure-toi que ces fonctions existent pour gérer les données

class CreationJoueur(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialisation du layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Ajouter les champs pour les données du joueur
        self.nom_input = TextInput(hint_text="Nom du joueur", font_size=18, multiline=False)
        self.hp_input = TextInput(hint_text="HP (ex: 100)", font_size=18, multiline=False, input_filter='int')
        self.mana_input = TextInput(hint_text="Mana (ex: 50)", font_size=18, multiline=False, input_filter='int')

        # Ajouter un bouton pour enregistrer le joueur
        btn_enregistrer = Button(text="Enregistrer le joueur", font_size=18, size_hint=(None, None), size=(200, 50))
        btn_enregistrer.bind(on_press=self.enregistrer_joueur)

        # Ajouter un label pour les erreurs éventuelles
        self.error_label = Label(text="", color=(1, 0, 0, 1), font_size=18)

        layout.add_widget(Label(text="Création d'un joueur", font_size=30, bold=True))
        layout.add_widget(self.nom_input)
        layout.add_widget(self.hp_input)
        layout.add_widget(self.mana_input)
        layout.add_widget(btn_enregistrer)
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def enregistrer_joueur(self, instance):
        # Récupérer les données du joueur
        nom = self.nom_input.text
        try:
            hp = int(self.hp_input.text)
            mana = int(self.mana_input.text)
        except ValueError:
            # Afficher une erreur si les HP ou mana ne sont pas des nombres valides
            self.error_label.text = "Les HP et le Mana doivent être des nombres entiers."
            return

        if not nom or hp <= 0 or mana <= 0:
            # Vérifier que tous les champs sont remplis correctement
            self.error_label.text = "Veuillez entrer un nom valide et des valeurs positives pour HP et Mana."
            return

        # Charger les données actuelles
        data = load_data()
        crit_result = False
        # Ajouter le nouveau joueur avec un ID unique
        new_id = len(data["joueurs"])  # Utiliser la taille actuelle pour générer un ID unique
        data["joueurs"].append({
            "nom": nom,
            "hp": hp,
            "mana": mana,
            "echec_critique_1": crit_result,
            "echec_critique_2": crit_result,
            "reussite_critique_1": crit_result,
            "reussite_critique_2": crit_result
        })

        # Sauvegarder les données
        save_data(data)

        # Mettre à jour l'écran de sélection des joueurs
        self.manager.get_screen('selection_joueur').creer_boutons_joueurs()

        # Afficher un message de succès et rediriger vers l'écran de sélection
        self.error_label.text = ""  # Réinitialiser l'erreur
        self.manager.current = 'selection_joueur'  # Rediriger vers la page de sélection des joueurs
