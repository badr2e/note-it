"""Ce fichier contient la classe MainMenuAdmin qui est une interface graphique qui permet à l'administrateur de supprimer un compte utilisateur"""


#----------------Importation des modules----------------


import tkinter as tk
from interface.deleteAccount import DeleteAccountPage


#----------------Classe MainMenuAdmin----------------


class MainMenuAdmin(tk.Frame):
    def __init__(self, master, db, home_page_ref, admin): # Constructeur de la classe MainMenuAdmin
        super().__init__(master)
        self.master = master
        self.db = db
        self.admin = admin 
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

        label_title = tk.Label(self.master, text="Menu Principal Admin", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        label_title.pack(pady=(20, 10))

        nombre_comptes = self.db.get_number_accounts() # Récupérer le nombre de comptes dans la base de données
        self.label_nombre_comptes = tk.Label(self.master, text=f"Nombre de comptes dans l'application : {nombre_comptes}", font=("Arial", 12, "bold"), bg="white", fg="black")
        self.label_nombre_comptes.pack(pady=(130,10))

        #---------Menu---------#

        btn_supprimer_compte = tk.Button(self.master, text="Supprimer un compte", command=self.delete_account, font=("Arial", 12, "bold"))
        btn_supprimer_compte.pack(pady=(10))

        btn_se_deconnecter = tk.Button(self.master, text="Se déconnecter", command=self.logout, font=("Arial", 12, "bold"))
        btn_se_deconnecter.pack(pady=10)

    def delete_account(self):
        DeleteAccountPage(self.master, self.db, self.admin)

    def logout(self):
        self.master.destroy()
        self.home_page_ref.logout()

    def on_close(self):
        self.master.quit()