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

        # Conteneur principal centré verticalement
        main_layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        
        # Layout pour centrer les éléments horizontalement
        center_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Titre
        label = Label(text="Bienvenue dans ArcaneSync", font_size=40, bold=True, size_hint=(1, None), height=60, halign='center')
        label.bind(size=label.setter('text_size'))  # Pour que le texte se centre bien

        # Boutons
        btn_joueur = Button(text="Joueur", font_size=18, size_hint=(1, None), height=50)
        btn_mj = Button(text="Mode MJ", font_size=18, size_hint=(1, None), height=50)
        btn_creation_joueur = Button(text="Créer un Joueur", font_size=18, size_hint=(1, None), height=50)

        # Ajouter les widgets au layout centré
        center_layout.add_widget(btn_joueur)
        center_layout.add_widget(btn_mj)
        center_layout.add_widget(btn_creation_joueur)

        # Ajouter les éléments au layout principal
        main_layout.add_widget(label)
        main_layout.add_widget(center_layout)

        # Ajout du layout à l'écran
        self.add_widget(main_layout)

        # Bind des boutons
        btn_joueur.bind(on_press=self.start_joueur)
        btn_mj.bind(on_press=self.start_mj)
        btn_creation_joueur.bind(on_press=self.start_creation_joueur)

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