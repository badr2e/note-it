"""Ce fichier contient la classe HomePage qui est la page d'accueil de l'application.
Elle contient deux parties : une partie pour se connecter et une partie pour créer un compte."""

#----------------Importation des modules----------------


import tkinter as tk # Importation du module tkinter pour l'interface graphique
from tkinter import messagebox # Importation du module messagebox de tkinter pour afficher des messages d'alerte
from interface.mainMenuUser import MainMenuUser # Importation de la classe MainMenuUser pour afficher le menu principal de l'utilisateur
from interface.mainMenuAdmin import MainMenuAdmin # Importation de la classe MainMenuAdmin pour afficher le menu principal de l'administrateur


#----------------Classe HomePage----------------


class HomePage(tk.Frame):
    def __init__(self, master, db): # Constructeur de la classe HomePage
        super().__init__(master) # Appel du constructeur de la classe parente Frame
        self.master = master # Fenêtre principale
        self.db = db 
        self.create_widgets() # Appel de la méthode pour créer les widgets de la page d'accueil

    def create_widgets(self):
        # Configuration de la fenêtre principale
        self.master.title("Note-it")
        self.master.iconbitmap('assets/favicon.ico')
        self.master.geometry("800x500")
        self.master.configure(bg="#0053f4")
        self.master.resizable(False, False) # Empêcher le redimensionnement de la fenêtre

        #---------Titre---------#

        label_title = tk.Label(self.master, text="Note-it : Agenda Personnel", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        label_title.pack(pady=(20, 10))

        #---------Container frame---------#

        frame_container = tk.Frame(self.master, bg="#0053f4")
        frame_container.pack(expand=True, fill='both')

        #---------Login frame---------#

        frame_login = tk.Frame(frame_container, bg="white", highlightbackground="black", highlightthickness=5)
        frame_login.pack(side="left", expand=True, fill='both', padx=(50, 10), pady=(10,40))

        label_login = tk.Label(frame_login, text="Se connecter", font=("Arial", 18, "bold"), bg="white")
        label_login.pack(pady=(75, 5))

        label_user_login = tk.Label(frame_login, text="Nom d'utilisateur", font=("Arial", 11), bg="white")
        label_user_login.pack(fill='x')

        self.entry_user_login = tk.Entry(frame_login, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_user_login.pack(pady=5, padx=10, fill='x')

        label_pass_login = tk.Label(frame_login, text="Mot de passe", bg="white", font=("Arial", 11))
        label_pass_login.pack(fill='x')

        self.entry_pass_login = tk.Entry(frame_login, show='*', bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_pass_login.pack(pady=5, padx=10, fill='x')

        self.entry_pass_login.bind("<Return>", lambda event: self.login()) # Appel de la méthode login lors de l'appui sur la touche Entrée

        btn_forgot = tk.Button(frame_login, text="Mot de passe oublié ?", border=0, fg="#0053f4", bg="white", font=("Arial", 11))
        btn_forgot.pack(pady=10)

        btn_login = tk.Button(frame_login, text="Se connecter", command=self.login, bg="#0053f4", fg="white", font=("Arial", 11)) # Bouton pour se connecter
        btn_login.pack(pady=(0,10))

        #---------Registration frame---------#

        frame_registration = tk.Frame(frame_container, bg="white", highlightbackground="black", highlightthickness=5)
        frame_registration.pack(side="right", expand=True, fill='both', padx=(10, 50), pady=(10,40))

        label_registration = tk.Label(frame_registration, text="Créer un compte", font=("Arial", 18, "bold"), bg="white")
        label_registration.pack(pady=(75, 5))

        label_user_register = tk.Label(frame_registration, text="Nom d'utilisateur", bg="white", font=("Arial", 11))
        label_user_register.pack(fill='x')

        self.entry_user_register = tk.Entry(frame_registration, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_user_register.pack(pady=5, padx=10, fill='x')

        label_email_register = tk.Label(frame_registration, text="Email", bg="white", font=("Arial", 11))
        label_email_register.pack(fill='x')

        self.entry_email_register = tk.Entry(frame_registration, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_email_register.pack(pady=5, padx=10, fill='x')

        label_pass_register = tk.Label(frame_registration, text="Mot de passe", bg="white", font=("Arial", 11))
        label_pass_register.pack(fill='x')

        self.entry_pass_register = tk.Entry(frame_registration, show='*', bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_pass_register.pack(pady=5, padx=10, fill='x')

        self.entry_pass_register.bind("<Return>", lambda event: self.register()) # Appel de la méthode register lors de l'appui sur la touche Entrée

        btn_register = tk.Button(frame_registration, text="S'enregistrer", command=self.register, bg="#0053f4", fg="white", font=("Arial", 11)) # Bouton pour enregistrer un utilisateur
        btn_register.pack(pady=10)

    def register(self): # Méthode pour enregistrer un utilisateur
        username = self.entry_user_register.get() # Récupération du nom d'utilisateur
        email = self.entry_email_register.get()
        password = self.entry_pass_register.get()
        success, message = self.db.register(email, username, password) # Appel de la méthode register de la classe DatabaseHandler pour récupérer le résultat de l'enregistrement
        if success:
            messagebox.showinfo("Succès", message) # Affichage d'un message de succès
            self.entry_user_register.delete(0, tk.END) # Effacement des champs de saisie
            self.entry_email_register.delete(0, tk.END)
            self.entry_pass_register.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", message) # Affichage d'un message d'erreur

    def login(self):
        username = self.entry_user_login.get() # Récupération du nom d'utilisateur
        password = self.entry_pass_login.get()
        account, message = self.db.login(username, password) # Appel de la méthode login de la classe DatabaseHandler pour récupérer le résultat de la connexion
        if account:
            messagebox.showinfo("Succès", message) # Affichage d'un message de succès
            if account[1] == 1: # Si l'utilisateur est un administrateur
                self.open_main_menu_admin(account) # Appel de la méthode open_main_menu_admin pour ouvrir le menu principal de l'administrateur
            else:
                self.open_main_menu_user(account) # Appel de la méthode open_main_menu_user pour ouvrir le menu principal de l'utilisateur
        else:
            messagebox.showerror("Erreur", message)
        self.entry_user_login.delete(0, tk.END) # Effacement des champs de saisie
        self.entry_pass_login.delete(0, tk.END)

    def open_main_menu_user(self, account): # Méthode pour ouvrir le menu principal de l'utilisateur
        self.master.withdraw() # Réduction de la fenêtre principale
        new_window = tk.Toplevel(self.master) # Création d'une nouvelle fenêtre
        MainMenuUser(new_window, self.db, self, account) # Création d'une instance de la classe MainMenuUser

    def open_main_menu_admin(self, account):
        self.master.withdraw()
        new_window = tk.Toplevel(self.master)
        MainMenuAdmin(new_window, self.db, self, account)

    def logout(self): # Méthode pour se déconnecter, cette méthode va être appelée depuis les menus
        self.master.deiconify() # Restauration de la fenêtre principale