from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from data_manager import load_data, save_data  # Assure-toi que ces fonctions existent pour gérer les données

class SelectionJoueur(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Titre de la sélection
        label = Label(text="Choisissez votre joueur", font_size=30, bold=True)

        # Ajouter le label au layout
        self.layout.add_widget(label)

        # Charger les joueurs existants et créer les boutons pour chacun d'eux
        self.creer_boutons_joueurs()

        self.add_widget(self.layout)

    def creer_boutons_joueurs(self):
        # Charger les données des joueurs
        data = load_data()

        # Supprimer les widgets existants (y compris les boutons et labels)
        self.layout.clear_widgets()

        # Ajouter le label au layout à nouveau (sinon il serait supprimé)
        self.layout.add_widget(Label(text="Choisissez votre joueur", font_size=30, bold=True))

        # Créer un bouton pour chaque joueur existant
        for index, joueur in enumerate(data["joueurs"]):
            # Créer le bouton de sélection du joueur
            btn_joueur = Button(
                text=joueur["nom"], font_size=18, size_hint=(None, None), size=(200, 50)
            )
            btn_joueur.bind(on_press=self.selectionner_joueur)
            btn_joueur.player_id = index  # Stocker l'ID du joueur dans le bouton

            # Créer le bouton de suppression
            btn_supprimer = Button(
                text="Supprimer", font_size=18, size_hint=(None, None), size=(100, 50)
            )
            btn_supprimer.bind(on_press=self.supprimer_joueur)
            btn_supprimer.player_id = index  # Stocker l'ID du joueur dans le bouton de suppression

            # Créer un layout horizontal pour les deux boutons
            bouton_layout = BoxLayout(orientation='horizontal', spacing=10)
            bouton_layout.add_widget(btn_joueur)
            bouton_layout.add_widget(btn_supprimer)

            # Ajouter le layout au layout principal
            self.layout.add_widget(bouton_layout)

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