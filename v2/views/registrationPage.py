"""Ce fichier est la page d'inscription de l'application. Elle permet à l'utilisateur de créer un compte."""


#----------------Importation des modules----------------


import tkinter as tk
from tkinter import messagebox


#----------------Classe RegistrationPage----------------


class RegistrationPage(tk.Frame):
    def __init__(self, parent, db): # On initialise la classe RegistrationPage.
        tk.Frame.__init__(self, parent)
        self.db = db
        self.parent = parent # Pour l'instant, on ne fait pas appel à la fenêtre parent, dans des versions futures, on pourrait l'utiliser pour revenir à la page de connexion ou pour se connecter automatiquement après l'inscription.
        self.configure(bg="#0053f4")
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Note-it : Agenda Personnel", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        title.pack(pady=(20))

        frame_registration = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_registration.pack(expand=True, fill='both', padx=(75, 75), pady=(0,40))

        label_registration = tk.Label(frame_registration, text="Créer un compte", font=("Arial", 18, "bold"), bg="white")
        label_registration.pack(pady=(55, 5))

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






