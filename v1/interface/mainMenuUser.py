"""Ce fichier contient la classe MainMenuUser qui est une interface graphique qui permet à l'utilisateur de voir les évènements, d'ajouter un évènement et de supprimer un évènement"""


#----------------Importation des modules----------------


import tkinter as tk # Importation du module tkinter pour l'interface graphique
from interface.addEvent import AddEventPage # Importation de la classe AddEventPage pour ajouter un évènement
from interface.deleteEvents import DeleteEventsPage # Importation de la classe DeleteEventsPage pour supprimer un évènement
from interface.showEvents import ShowEventsPage # Importation de la classe ShowEventsPage pour afficher les évènements


#----------------Classe MainMenuUser----------------


class MainMenuUser(tk.Frame):
    def __init__(self, master, db, home_page_ref,user): # Constructeur de la classe MainMenuUser
        super().__init__(master)
        self.master = master
        self.db = db
        self.user = user # Sauvegarder l'utilisateur connecté
        self.home_page_ref = home_page_ref  # Sauvegarder la référence à HomePage
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close) # Appeler la méthode on_close lors de la fermeture de la fenêtre

    def create_widgets(self):
        # Configuration de la fenêtre principale
        self.master.title("Note-it")
        self.master.iconbitmap('assets/favicon.ico')
        self.master.geometry("800x500")
        self.master.configure(bg="#0053f4")
        self.master.resizable(False, False)

        #---------Titre---------#

        label_title = tk.Label(self.master, text="Menu Principal Utilisateur", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        label_title.pack(pady=(20, 10))

        #---------Menu---------#

        btn_show_events = tk.Button(self.master, text="Afficher les évènements", command=self.show_events, font=("Arial", 12, "bold"))
        btn_show_events.pack(pady=(100,10))

        btn_add_event = tk.Button(self.master, text="Ajouter un évènement", command=self.add_event, font=("Arial", 12, "bold"))
        btn_add_event.pack(pady=(10))

        btn_delete_event = tk.Button(self.master, text="Supprimer un évènement", command=self.delete_event, font=("Arial", 12, "bold"))
        btn_delete_event.pack(pady=(10))

        btn_logout = tk.Button(self.master, text="Se déconnecter", command=self.logout, font=("Arial", 12, "bold"))
        btn_logout.pack(pady=10)

    # En fonction du choix du l'utilisateur on affiche la page correspondante
        
    def show_events(self):
        ShowEventsPage(self.master, self.db, self.user)

    def add_event(self):
        AddEventPage(self.master, self.db, self.user)

    def delete_event(self):
        DeleteEventsPage(self.master, self.db, self.user)

    def logout(self): # Méthode pour se déconnecter
        self.master.destroy() # Fermer la fenêtre actuelle
        self.home_page_ref.logout() # On appelle la méthode logout de HomePage qui va faire réapparaître la page d'accueil

    def on_close(self):
        self.master.quit() # On quitte l'application et on arrête la boucle principale