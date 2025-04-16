from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from data_manager import load_data, save_data  # Assure-toi que ces fonctions existent pour gérer les données

class CreationJoueur(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Barre supérieure avec bouton retour
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        btn_retour = Button(text="< Accueil", size_hint=(None, 1), width=120, font_size=14)
        btn_retour.bind(on_press=self.retour_accueil)
        top_bar.add_widget(btn_retour)

        # Layout central pour le contenu
        content_layout = BoxLayout(orientation='vertical', spacing=10)

        self.nom_input = TextInput(hint_text="Nom du joueur", font_size=18, multiline=False)
        self.hp_input = TextInput(hint_text="HP (ex: 100)", font_size=18, multiline=False, input_filter='int')
        self.mana_input = TextInput(hint_text="Mana (ex: 50)", font_size=18, multiline=False, input_filter='int')

        btn_enregistrer = Button(text="Enregistrer le joueur", font_size=18, size_hint=(None, None), size=(200, 50))
        btn_enregistrer.bind(on_press=self.enregistrer_joueur)

        self.error_label = Label(text="", color=(1, 0, 0, 1), font_size=18)

        content_layout.add_widget(Label(text="Création d'un joueur", font_size=30, bold=True))
        content_layout.add_widget(self.nom_input)
        content_layout.add_widget(self.hp_input)
        content_layout.add_widget(self.mana_input)
        content_layout.add_widget(btn_enregistrer)
        content_layout.add_widget(self.error_label)

        # Ajouter top bar et contenu au layout principal
        main_layout.add_widget(top_bar)
        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def retour_accueil(self, instance):
        self.manager.current = 'accueil'

    def enregistrer_joueur(self, instance):
        nom = self.nom_input.text
        try:
            hp = int(self.hp_input.text)
            mana = int(self.mana_input.text)
        except ValueError:
            self.error_label.text = "Les HP et le Mana doivent être des nombres entiers."
            return

        if not nom or hp <= 0 or mana <= 0:
            self.error_label.text = "Veuillez entrer un nom valide et des valeurs positives pour HP et Mana."
            return

        data = load_data()
        crit_result = False
        new_id = len(data["joueurs"])
        data["joueurs"].append({
            "nom": nom,
            "hp": hp,
            "mana": mana,
            "echec_critique_1": crit_result,
            "echec_critique_2": crit_result,
            "reussite_critique_1": crit_result,
            "reussite_critique_2": crit_result
        })

        save_data(data)
        self.manager.get_screen('selection_joueur').creer_boutons_joueurs()
        self.error_label.text = ""
        self.manager.current = 'selection_joueur'
