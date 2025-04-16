from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock  # 👈 Pour les mises à jour régulières
from data_manager import load_data, save_data

class Serveur(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = load_data()

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        label = Label(text="Interface Maître du Jeu", font_size=30)

        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        self.checkbox_widgets = []
        self.player_labels = []
        self.critique_widgets = []

        for i, joueur in enumerate(self.data["joueurs"]):
            joueur_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150)

            top_line = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            checkbox = CheckBox()
            label_joueur = Label(text=f"{joueur['nom']} - HP: {joueur['hp']} Mana: {joueur['mana']}", font_size=18)
            top_line.add_widget(checkbox)
            top_line.add_widget(label_joueur)

            self.checkbox_widgets.append((checkbox, i))
            self.player_labels.append(label_joueur)

            # Ligne Échec critique
            echec_line = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=10)
            echec_label = Label(text="Échec critique :", size_hint=(0.4, 1))
            cb_ec1 = CheckBox(active=joueur.get("echec_critique_1", False))
            cb_ec2 = CheckBox(active=joueur.get("echec_critique_2", False))
            cb_ec1.bind(active=self.update_critiques)
            cb_ec2.bind(active=self.update_critiques)
            echec_line.add_widget(echec_label)
            echec_line.add_widget(cb_ec1)
            echec_line.add_widget(cb_ec2)

            # Ligne Réussite critique
            reussite_line = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=10)
            reussite_label = Label(text="Réussite critique :", size_hint=(0.4, 1))
            cb_rc1 = CheckBox(active=joueur.get("reussite_critique_1", False))
            cb_rc2 = CheckBox(active=joueur.get("reussite_critique_2", False))
            cb_rc1.bind(active=self.update_critiques)
            cb_rc2.bind(active=self.update_critiques)
            reussite_line.add_widget(reussite_label)
            reussite_line.add_widget(cb_rc1)
            reussite_line.add_widget(cb_rc2)

            self.critique_widgets.append((i, cb_ec1, cb_ec2, cb_rc1, cb_rc2))

            joueur_layout.add_widget(top_line)
            joueur_layout.add_widget(echec_line)
            joueur_layout.add_widget(reussite_line)

            scroll_layout.add_widget(joueur_layout)

        scroll_view = ScrollView(size_hint=(1, None), size=(self.width, 300))
        scroll_view.add_widget(scroll_layout)

        self.input_degats = TextInput(hint_text="Entrez les dégâts à infliger", multiline=False, input_filter='int', font_size=18, size_hint=(1, 0.2))
        self.input_mana = TextInput(hint_text="Entrez la Mana à infliger", multiline=False, input_filter='int', font_size=18, size_hint=(1, 0.2))

        btn_degats = Button(text="Infliger Dégâts", font_size=18)
        btn_degats.bind(on_press=self.infliger_degats)

        btn_mana = Button(text="Infliger Mana", font_size=18)
        btn_mana.bind(on_press=self.infliger_mana)

        btn_hp = Button(text="Ajouter 10 HP", font_size=18)
        btn_hp.bind(on_press=self.ajouter_hp)

        btn_mana_ajout = Button(text="Ajouter 10 Mana", font_size=18)
        btn_mana_ajout.bind(on_press=self.ajouter_mana)

        btn_retour = Button(text="Retour à l'accueil", font_size=18)
        btn_retour.bind(on_press=self.retour_accueil)

        self.layout.add_widget(label)
        self.layout.add_widget(scroll_view)
        self.layout.add_widget(self.input_degats)
        self.layout.add_widget(self.input_mana)
        self.layout.add_widget(btn_degats)
        self.layout.add_widget(btn_mana)
        self.layout.add_widget(btn_hp)
        self.layout.add_widget(btn_mana_ajout)
        self.layout.add_widget(btn_retour)

        self.add_widget(self.layout)

        # ⏱️ Planifie une mise à jour régulière des stats
        Clock.schedule_interval(self.refresh_stats, 2)

    def update_critiques(self, checkbox, value):
        for index, ec1, ec2, rc1, rc2 in self.critique_widgets:
            self.data["joueurs"][index]["echec_critique_1"] = ec1.active
            self.data["joueurs"][index]["echec_critique_2"] = ec2.active
            self.data["joueurs"][index]["reussite_critique_1"] = rc1.active
            self.data["joueurs"][index]["reussite_critique_2"] = rc2.active
        save_data(self.data)

    def infliger_degats(self, instance):
        try:
            degats = int(self.input_degats.text)
            for checkbox, index in self.checkbox_widgets:
                if checkbox.active:
                    joueur = self.data["joueurs"][index]
                    joueur["hp"] = max(0, joueur["hp"] - degats)
                    self.data["joueurs"][index] = joueur
                    save_data(self.data)
                    self.player_labels[index].text = f"{joueur['nom']} - HP: {joueur['hp']} Mana: {joueur['mana']}"
                    self.input_degats.text = ""
        except ValueError:
            pass

    def infliger_mana(self, instance):
        try:
            mana = int(self.input_mana.text)
            for checkbox, index in self.checkbox_widgets:
                if checkbox.active:
                    joueur = self.data["joueurs"][index]
                    joueur["mana"] = max(0, joueur["mana"] - mana)
                    self.data["joueurs"][index] = joueur
                    save_data(self.data)
                    self.player_labels[index].text = f"{joueur['nom']} - HP: {joueur['hp']} Mana: {joueur['mana']}"
                    self.input_mana.text = ""
        except ValueError:
            pass

    def ajouter_hp(self, instance):
        for checkbox, index in self.checkbox_widgets:
            if checkbox.active:
                joueur = self.data["joueurs"][index]
                joueur["hp"] += 10
                self.data["joueurs"][index] = joueur
                save_data(self.data)
                self.player_labels[index].text = f"{joueur['nom']} - HP: {joueur['hp']} Mana: {joueur['mana']}"

    def ajouter_mana(self, instance):
        for checkbox, index in self.checkbox_widgets:
            if checkbox.active:
                joueur = self.data["joueurs"][index]
                joueur["mana"] += 10
                self.data["joueurs"][index] = joueur
                save_data(self.data)
                self.player_labels[index].text = f"{joueur['nom']} - HP: {joueur['hp']} Mana: {joueur['mana']}"

    def retour_accueil(self, instance):
        self.manager.current = 'accueil'

    def refresh_stats(self, dt):
        new_data = load_data()  # Charger les nouvelles données

        # Vérifie que la liste des joueurs dans new_data existe et n'est pas vide
        if "joueurs" not in new_data or not new_data["joueurs"]:
            print("Aucun joueur trouvé dans les nouvelles données.")
            return

        # Vérifie si la liste des joueurs est différente de celle existante
        min_len = min(len(new_data["joueurs"]), len(self.data["joueurs"]))

        # Parcours les joueurs existants jusqu'à la longueur minimale des deux listes
        for i in range(min_len):
            joueur = new_data["joueurs"][i]
            ancien = self.data["joueurs"][i]

            # Vérifie les changements de HP et Mana
            if joueur["hp"] != ancien["hp"] or joueur["mana"] != ancien["mana"]:
                self.player_labels[i].text = f"{joueur['nom']} - HP: {joueur['hp']} Mana: {joueur['mana']}"

        # Si la nouvelle liste des joueurs est plus longue, ajoute les nouveaux joueurs
        for i in range(min_len, len(new_data["joueurs"])):
            joueur = new_data["joueurs"][i]
            self.data["joueurs"].append(joueur)
            self.player_labels.append(Label(text=f"{joueur['nom']} - HP: {joueur['hp']} Mana: {joueur['mana']}"))
        
        # Met à jour les données locales avec les nouvelles données
        self.data = new_data