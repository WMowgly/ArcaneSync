from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from data_manager import load_data, save_data
from kivy.uix.progressbar import ProgressBar

class ClientScreen(Screen):
    def __init__(self, joueur_id, **kwargs):
        super().__init__(**kwargs)

        self.joueur_id = joueur_id
        print(f"Chargement des données pour le joueur {self.joueur_id}")

        # Charger les données
        self.data = load_data()
        print(f"Données chargées : {self.data}")

        # Vérifier si la liste des joueurs est vide
        if not self.data["joueurs"]:
            # Afficher un message d'erreur ou rediriger vers l'écran de création de joueur
            print("Aucun joueur disponible. Veuillez ajouter un joueur.")
            # Utiliser Clock.schedule_once pour s'assurer que le manager est prêt
            Clock.schedule_once(self.rediriger_creation_joueur, 0.1)
            return  # Sortir de la fonction pour éviter l'initialisation de l'écran

        # Vérifier si l'ID du joueur est valide
        if joueur_id < 0 or joueur_id >= len(self.data["joueurs"]):
            print("ID du joueur invalide. Rediriger vers la page de sélection.")
            # Utiliser Clock.schedule_once pour s'assurer que le manager est prêt
            Clock.schedule_once(self.rediriger_selection_joueur, 0.1)
            return  # Sortir de la fonction pour éviter l'initialisation de l'écran

        # Si des joueurs existent et que l'ID est valide, récupérer les données du joueur
        self.hp = self.data["joueurs"][joueur_id]["hp"]
        self.mana = self.data["joueurs"][joueur_id]["mana"]
        print(f"HP du joueur : {self.hp}, Mana du joueur : {self.mana}")

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Statistiques du joueur
        self.hp_label = Label(text=f"HP : {self.hp}", font_size=22, color=(1, 0, 0, 1))
        self.mana_label = Label(text=f"Mana : {self.mana}", font_size=22, color=(0, 0, 1, 1))

        self.hp_bar = ProgressBar(value=self.hp, max=100, size_hint=(1, None), height=20)
        self.mana_bar = ProgressBar(value=self.mana, max=50, size_hint=(1, None), height=20)

        # Labels pour les critiques
        self.echec_label = Label(text="Échecs critiques : 0", font_size=18)
        self.reussite_label = Label(text="Réussites critiques : 0", font_size=18)

        # Champs d'action
        self.input_degats = TextInput(hint_text="Entrer les dégâts", multiline=False, input_filter='int', font_size=18)
        self.input_sort = TextInput(hint_text="Entrer la Mana pour un sort", multiline=False, input_filter='int', font_size=18)

        btn_degats = Button(text="Recevoir les dégâts", font_size=18)
        btn_degats.bind(on_press=self.recevoir_degats)

        btn_sort = Button(text="Lancer un Sort", font_size=18)
        btn_sort.bind(on_press=self.lancer_sort)

        btn_retour = Button(text="Retour à l'accueil", font_size=18)
        btn_retour.bind(on_press=self.retour_accueil)

        layout.add_widget(self.hp_label)
        layout.add_widget(self.hp_bar)
        layout.add_widget(self.mana_label)
        layout.add_widget(self.mana_bar)
        layout.add_widget(self.echec_label)
        layout.add_widget(self.reussite_label)
        layout.add_widget(self.input_degats)
        layout.add_widget(self.input_sort)
        layout.add_widget(btn_degats)
        layout.add_widget(btn_sort)
        layout.add_widget(btn_retour)

        self.add_widget(layout)
        print("Widgets ajoutés avec succès.")

        # Mise à jour automatique toutes les 2 secondes
        Clock.schedule_interval(self.refresh_stats, 2)

    def rediriger_creation_joueur(self, dt):
        if self.manager:  # Vérifier que le manager est bien disponible
            self.manager.current = 'creation_joueur'
        else:
            print("Erreur : Manager non disponible.")

    def rediriger_selection_joueur(self, dt):
        if self.manager:  # Vérifier que le manager est bien disponible
            self.manager.current = 'selection_joueur'
        else:
            print("Erreur : Manager non disponible.")

    def refresh_stats(self, dt):
        data = load_data()

        # Vérifier que l'ID du joueur est valide avant de continuer
        if self.joueur_id < len(data["joueurs"]):
            joueur = data["joueurs"][self.joueur_id]

            # Mise à jour HP / Mana
            if joueur["hp"] != self.hp or joueur["mana"] != self.mana:
                self.hp = joueur["hp"]
                self.mana = joueur["mana"]
                self.hp_label.text = f"HP : {self.hp}"
                self.mana_label.text = f"Mana : {self.mana}"
                self.hp_bar.value = self.hp
                self.mana_bar.value = self.mana

            # Mise à jour critiques
            nb_echec = int(joueur.get("echec_critique_1", False)) + int(joueur.get("echec_critique_2", False))
            nb_reussite = int(joueur.get("reussite_critique_1", False)) + int(joueur.get("reussite_critique_2", False))

            self.echec_label.text = f"Échecs critiques : {nb_echec}"
            self.reussite_label.text = f"Réussites critiques : {nb_reussite}"

    def recevoir_degats(self, instance):
        try:
            degats = int(self.input_degats.text)
            self.hp = max(0, self.hp - degats)
            self.hp_label.text = f"HP : {self.hp}"
            self.hp_bar.value = self.hp
            self.sauvegarder()
        except ValueError:
            pass

    def lancer_sort(self, instance):
        try:
            mana_utilisee = int(self.input_sort.text)
            if mana_utilisee <= self.mana:
                self.mana -= mana_utilisee
                self.mana_label.text = f"Mana : {self.mana}"
                self.mana_bar.value = self.mana
                self.sauvegarder()
        except ValueError:
            pass

    def sauvegarder(self):
        self.data["joueurs"][self.joueur_id]["hp"] = self.hp
        self.data["joueurs"][self.joueur_id]["mana"] = self.mana
        save_data(self.data)

    def retour_accueil(self, instance):
        self.manager.current = 'accueil'