from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from data_manager import load_data, save_data  # Assure-toi que ces fonctions existent pour gérer les données

class SelectionJoueur(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Layout principal vertical (haut, centre, bas)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # ---- HAUT : Barre avec bouton retour ----
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        btn_retour = Button(text="< Accueil", size_hint=(None, 1), width=100)
        btn_retour.bind(on_press=self.retour_accueil)
        top_bar.add_widget(btn_retour)
        self.main_layout.add_widget(top_bar)

        # ---- CENTRE : Layout des joueurs (sera rempli dynamiquement) ----
        self.layout_joueurs = BoxLayout(orientation='vertical', spacing=10)
        self.main_layout.add_widget(self.layout_joueurs)

        # ---- BAS : Bouton création joueur ----
        btn_creation_joueur = Button(
            text="Créer un nouveau joueur",
            font_size=18,
            size_hint=(1, None),
            height=50
        )
        btn_creation_joueur.bind(on_press=self.aller_creation_joueur)
        self.main_layout.add_widget(btn_creation_joueur)

        self.add_widget(self.main_layout)

        # Charger les boutons de joueurs
        self.creer_boutons_joueurs()

    def creer_boutons_joueurs(self):
        # Charger les données des joueurs
        data = load_data()

        # Vider l'ancien contenu
        self.layout_joueurs.clear_widgets()

        # Ajouter un titre
        self.layout_joueurs.add_widget(Label(text="Choisissez votre joueur", font_size=30, bold=True))

        # Créer les boutons pour chaque joueur
        for index, joueur in enumerate(data["joueurs"]):
            btn_joueur = Button(
                text=joueur["nom"], font_size=18, size_hint=(None, None), size=(200, 50)
            )
            btn_joueur.bind(on_press=self.selectionner_joueur)
            btn_joueur.player_id = index

            btn_supprimer = Button(
                text="Supprimer", font_size=18, size_hint=(None, None), size=(100, 50)
            )
            btn_supprimer.bind(on_press=self.supprimer_joueur)
            btn_supprimer.player_id = index

            ligne = BoxLayout(orientation='horizontal', spacing=10)
            ligne.add_widget(btn_joueur)
            ligne.add_widget(btn_supprimer)

            self.layout_joueurs.add_widget(ligne)

    def selectionner_joueur(self, instance):
        # Vérifier si l'ID du joueur est valide avant de continuer
        data = load_data()
        if instance.player_id < len(data["joueurs"]):
            self.manager.get_screen('client').joueur_id = instance.player_id
            self.manager.current = 'client'
        else:
            print("ID de joueur invalide, redirection vers la sélection.")
            self.manager.current = 'selection_joueur'

    def supprimer_joueur(self, instance):
        # Récupérer l'ID du joueur à supprimer
        player_id = instance.player_id

        # Charger les données actuelles
        data = load_data()

        # Supprimer le joueur de la liste des joueurs
        del data["joueurs"][player_id]

        # Réajuster les indices des joueurs suivants
        for i in range(player_id, len(data["joueurs"])):
            data["joueurs"][i]["id"] = i  # Mettre à jour l'ID des joueurs après la suppression

        # Sauvegarder les données après suppression
        save_data(data)

        # Mettre à jour l'interface en récréant les boutons
        self.creer_boutons_joueurs()

    def aller_creation_joueur(self, instance):
        self.manager.current = 'creation_joueur'

    def retour_accueil(self, instance):
        self.manager.current = 'accueil'

