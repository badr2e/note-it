import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class DeleteAccountPage(tk.Frame):
    def __init__(self, parent, db, account):
        tk.Frame.__init__(self, parent)
        self.db = db
        self.account = account
        self.configure(bg="#0053f4")
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self, text="Supprimer un compte", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        title.pack(pady=(20))

        frame_listbox = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_listbox.pack(expand=True, fill='both', padx=30, pady=(0, 20))

        scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL) # Ajout d'une barre de défilement à droite et qui se remplit verticalement
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(frame_listbox, yscrollcommand=scrollbar.set, font=("Arial", 11), bg="white", fg="black") # Création d'une liste pour afficher les comptes, on ne permet pas la sélection multiple
        self.listbox.pack(expand=True, fill='both')

        scrollbar.config(command=self.listbox.yview) # Configuration de la barre de défilement pour se synchroniser avec la liste

        btn_delete = tk.Button(self, text="Supprimer le compte sélectionné", command=self.delete_selected, font=("Arial", 14)) # On assigne la méthode delete_selected au bouton
        btn_delete.pack(pady=(10, 20))

        self.load_accounts() # Charger les comptes dans la liste

    def load_accounts(self):
        self.listbox.delete(0, tk.END) # Après avoir supprimer un compte, cela va permettre après de "recharger" la liste
        accounts = self.db.get_all_accounts() # On récupère tous les comptes
        for account in accounts:
            idUser, email, username = account[0], account[2], account[3]
            self.listbox.insert(tk.END, f"Id : {idUser} - Email : {email} - Nom d'utilisateur : {username}") # On insère les comptes dans la liste

    def delete_selected(self):
        selected_index = self.listbox.curselection()  # On récupère l'index du compte sélectionné dans la liste
        if not selected_index:  # Si aucun compte n'est sélectionné, on affiche un message d'erreur
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un compte à supprimer.")
            return
        selected_account = self.listbox.get(selected_index) # On récupère le compte sélectionné et le texte affiché associé
        id_user = selected_account.split(" - ")[0][5:]  # Extraction de l'id de l'utilisateur du compte sélectionné
        confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le compte sélectionné : {selected_account} ?")
        if confirmation: 
            password = self.ask_for_password()  # Demande du mot de passe de l'administrateur pour confirmer la suppression
            if password is not None: 
                account, message = self.db.login(self.account[3], password)  
                if account: # Si le mot de passe est correct, on peut supprimer le compte
                    success, message = self.db.delete_account(int(id_user), self.account[0]) # Suppression du compte de la base de données
                    if success: 
                        messagebox.showinfo("Succès", message)
                        self.load_accounts() # On recharge la listbox
                    else: 
                        messagebox.showerror("Erreur", message)
                else:
                    messagebox.showerror("Erreur", "Mot de passe incorrect")

    def ask_for_password(self): # Méthode pour demander le mot de passe de l'administrateur
        password = simpledialog.askstring("Vérification", "Veuillez entrer votre mot de passe pour confirmer la suppression :",show="*")
        return password