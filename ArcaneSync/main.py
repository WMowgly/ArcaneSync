from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from mj import Serveur  # Import de l'interface pour le MJ
from client import ClientScreen  # Import de l'interface pour le joueur
from creation_joueur import CreationJoueur  # Import du nouvel écran pour créer un joueur
from selection_joueur import SelectionJoueur  # Import du nouvel écran pour sélectionner un joueur

class Accueil(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Titre de l'interface
        label = Label(text="Bienvenue dans ArcaneSync", font_size=50, bold=True)
        btn_joueur = Button(text="Joueur", font_size=18, size_hint=(None, None), size=(200, 50))
        btn_mj = Button(text="Mode MJ", font_size=18, size_hint=(None, None), size=(200, 50))
        btn_creation_joueur = Button(text="Créer un Joueur", font_size=18, size_hint=(None, None), size=(200, 50))  # Nouveau bouton

        layout.add_widget(label)
        layout.add_widget(btn_joueur)
        layout.add_widget(btn_mj)
        layout.add_widget(btn_creation_joueur)  # Ajouter le bouton de création de joueur

        btn_joueur.bind(on_press=self.start_joueur)
        btn_mj.bind(on_press=self.start_mj)
        btn_creation_joueur.bind(on_press=self.start_creation_joueur)  # Lier à la fonction pour créer un joueur

        self.add_widget(layout)

    def start_joueur(self, instance):
        # Redirige vers l'écran de sélection du joueur
        self.manager.current = 'selection_joueur'

    def start_mj(self, instance):
        # Redirige vers l'écran du Maître du Jeu (MJ)
        self.manager.current = 'serveur'

    def start_creation_joueur(self, instance):
        # Redirige vers l'écran de création du joueur
        self.manager.current = 'creation_joueur'


class ArcaneSyncApp(App):
    def build(self):
        screen_manager = ScreenManager()

        # Ajout des écrans
        screen_manager.add_widget(Accueil(name='accueil'))  # Écran d'accueil
        screen_manager.add_widget(SelectionJoueur(name='selection_joueur'))  # Écran de sélection du joueur

        # Initialisation de ClientScreen sans joueur_id, puis il sera modifié dynamiquement
        client_screen = ClientScreen(joueur_id=0, name='client')  # Passer un joueur_id par défaut
        screen_manager.add_widget(client_screen)  # Interface joueur

        screen_manager.add_widget(Serveur(name='serveur'))  # Interface Maître du Jeu

        # Ajouter l'écran de création du joueur
        screen_manager.add_widget(CreationJoueur(name='creation_joueur'))  # Interface de création du joueur

        return screen_manager

if __name__ == '__main__':
    ArcaneSyncApp().run()