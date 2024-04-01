"""Ce fichier est le controlleur de l'application. Il permet de gérer les différentes pages de l'application Note-it.
À l'initialisation de la classe Controller, on crée une instance de la classe tk.Tk qui représente la fenêtre principale de l'application et on lance la page de connexion."""


#----------------Importation des modules----------------


import tkinter as tk
from views.loginPage import LoginPage
from views.registrationPage import RegistrationPage
from views.showEventsPage import ShowEventsPage
from views.addCategoryPage import AddCategoryPage
from views.addEventPage import AddEventPage
from views.deleteEventsPage import DeleteEventsPage
from views.deleteAccountPage import DeleteAccountPage


#----------------Classe Controller----------------


class Controller(tk.Tk):
    def __init__(self, db): # On initialise la classe Controller et notre fenêtre principale.
        tk.Tk.__init__(self)
        self.title("Note-it")
        self.iconbitmap('assets/favicon.ico')
        self.geometry("800x500")
        self.resizable(False, False)
        self.db = db
        self.account = None # On initialise le compte de l'utilisateur à None.
        self.show_home_page(LoginPage) # On affiche la page de connexion.

    def show_home_page(self, page_class): # Fonction permettant d'afficher la page d'accueil (connexion ou inscription).
        self.clear_window() # On efface le contenu de la fenêtre.
        self.home_menu() # On affiche le menu de la page d'accueil.
        page = page_class(self, self.db) # On crée une instance de la page passée en paramètre.
        page.pack(fill='both', expand=True) # On affiche la page.
        page.tkraise() # On met la page au premier plan.
    
    def show_page(self, page_class, account): # Fonction permettant d'afficher une page de l'application.
        self.clear_window()
        self.user_menu() if page_class != DeleteAccountPage else self.admin_menu() # On affiche le menu de l'utilisateur ou de l'administrateur en fonction de la page affichée.
        page = page_class(self.db, account)
        page.pack(fill='both', expand=True)
        page.tkraise()
    
    # Fonctions permettant d'afficher les différentes pages de l'application.

    def show_login_page(self):
        self.show_home_page(LoginPage)
    
    def show_registration_page(self):
        self.show_home_page(RegistrationPage)
   
    def add_category_page(self, account):
        self.show_page(AddCategoryPage, account)

    def add_event_page(self, account):
        self.show_page(AddEventPage, account)

    def delete_events_page(self, account):
        self.show_page(DeleteEventsPage, account)

    def delete_account_page(self, account):
        self.show_page(DeleteAccountPage, account)

    # Fonctions permettant de gérer les menus de l'application.
    
    def home_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        login_menu = tk.Menu(menubar, tearoff=0)
        login_menu.add_command(label="Se connecter", command=lambda: self.show_home_page(LoginPage))
        menubar.add_cascade(label="Se connecter", menu=login_menu)

        register_menu = tk.Menu(menubar, tearoff=0)
        register_menu.add_command(label="S'inscrire", command=lambda: self.show_home_page(RegistrationPage))
        menubar.add_cascade(label="S'inscrire", menu=register_menu)

        quit_menu = tk.Menu(menubar, tearoff=0)
        quit_menu.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Quitter", menu=quit_menu)
        
    def user_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        show_events_menu = tk.Menu(menubar, tearoff=0)
        show_events_menu.add_command(label="Afficher les évènements", command=lambda: self.show_page(ShowEventsPage, self.account))
        menubar.add_cascade(label="Afficher les évènements", menu=show_events_menu)

        add_category_menu = tk.Menu(menubar, tearoff=0)
        add_category_menu.add_command(label="Ajouter une catégorie", command=lambda: self.show_page(AddCategoryPage, self.account))
        menubar.add_cascade(label="Ajouter une catégorie", menu=add_category_menu)

        add_event_menu = tk.Menu(menubar, tearoff=0)
        add_event_menu.add_command(label="Ajouter un évènement", command=lambda: self.show_page(AddEventPage, self.account))
        menubar.add_cascade(label="Ajouter un évènement", menu=add_event_menu)

        delete_event_menu = tk.Menu(menubar, tearoff=0)
        delete_event_menu.add_command(label="Supprimer un évènement", command=lambda:self.show_page(DeleteEventsPage, self.account))
        menubar.add_cascade(label="Supprimer un évènement", menu=delete_event_menu)

        logout_menu = tk.Menu(menubar, tearoff=0)
        logout_menu.add_command(label="Se déconnecter", command=lambda: self.logout())
        menubar.add_cascade(label="Se déconnecter", menu=logout_menu)

    def admin_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        delete_account_menu = tk.Menu(menubar, tearoff=0)
        delete_account_menu.add_command(label="Supprimer un compte", command=lambda: self.show_page(DeleteAccountPage, self.account))
        menubar.add_cascade(label="Supprimer un compte", menu=delete_account_menu)

        logout_menu = tk.Menu(menubar, tearoff=0)
        logout_menu.add_command(label="Se déconnecter", command=lambda: self.logout())
        menubar.add_cascade(label="Se déconnecter", menu=logout_menu)
    
    # Fonctions permettant de gérer la connexion et la déconnexion de l'utilisateur.
    
    def login_success(self, account):
        self.account = account
        if account[1] == 1:
            self.show_page(DeleteAccountPage, account)
        else:
            self.show_page(ShowEventsPage, account)
    
    def logout(self):
        self.account = None
        self.show_home_page(LoginPage)
    
    def clear_window(self):
        for widget in self.winfo_children(): # On parcourt les widgets de la fenêtre.
            widget.destroy() # On détruit chaque widget.