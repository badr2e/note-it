import tkinter as tk
from tkinter import messagebox

class LoginPage(tk.Frame):
    def __init__(self, parent, db):
        tk.Frame.__init__(self, parent)
        self.db = db
        self.parent = parent
        self.configure(bg="#0053f4")
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self, text="Note-it : Agenda Personnel", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        title.pack(pady=(20))

        frame_login = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_login.pack(expand=True, fill='both', padx=(75, 75), pady=(0,40))

        label_login = tk.Label(frame_login, text="Se connecter", font=("Arial", 18, "bold"), bg="white")
        label_login.pack(pady=(65, 5))

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
        

    def login(self):
        username = self.entry_user_login.get()
        password = self.entry_pass_login.get()
        account, message = self.db.login(username, password)
        if account:
            messagebox.showinfo("Succès", message)
            self.parent.login_success(account)
        else:
            messagebox.showerror("Erreur", message)
