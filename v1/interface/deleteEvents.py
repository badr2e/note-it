"""Ce fichier contient la classe DeleteEventsPage qui est une interface graphique qui permet à l'utilisateur de supprimer un évènement"""


#----------------Importation des modules----------------


import tkinter as tk
from tkinter import messagebox
from datetime import datetime


#----------------Classe DeleteEventsPage----------------


class DeleteEventsPage(tk.Toplevel):
    def __init__(self, master, db, user): # Constructeur de la classe DeleteEventsPage
        super().__init__(master) 
        self.db = db
        self.user = user
        self.create_widgets()

    def create_widgets(self):
        # Configuration de la fenêtre
        self.title("Note-it")
        self.iconbitmap('assets/favicon.ico')
        self.geometry("800x500")
        self.configure(bg="#0053f4")
        self.resizable(False, False)

        label_title = tk.Label(self, text="Supprimer un évènement", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        label_title.pack(pady=(20, 10))

        #---------Frame Container Listbox---------#

        frame_listbox = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_listbox.pack(expand=True, fill='both', padx=30, pady=(0, 20))

        scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL) # Ajout d'une barre de défilement à droite et qui se remplit verticalement
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(frame_listbox, yscrollcommand=scrollbar.set, selectmode=tk.MULTIPLE, font=("Arial", 11), bg="white", fg="black") # Création d'une liste pour afficher les évènements, on permet la sélection multiple
        self.listbox.pack(expand=True, fill='both')

        scrollbar.config(command=self.listbox.yview) # Configuration de la barre de défilement pour se synchroniser avec la liste

        btn_delete = tk.Button(self, text="Supprimer sélection", command=self.delete_selected, font=("Arial", 14)) # On assigne la méthode delete_selected au bouton
        btn_delete.pack(pady=(10, 20))

        self.load_events()

    def load_events(self):
        self.listbox.delete(0, tk.END) # Après avoir supprimer un évènement, cela va permettre après de "recharger" la liste
        events = self.db.get_all_events(self.user) # On récupère tous les évènements de l'utilisateur
        for event in events:
            idEvent, title, description, dateFrom, dateTo = event[0], *event[2:6] 
            formatted_dateFrom = DeleteEventsPage.format_date_french(dateFrom) # On formate la date de début en français
            formatted_dateTo = DeleteEventsPage.format_date_french(dateTo) # On formate la date de fin en français
            self.listbox.insert(tk.END, (f"N°{idEvent} - {title} - {description} - Du {formatted_dateFrom} au {formatted_dateTo}")) # On insère les évènements dans la liste

    @staticmethod
    def format_date_french(date_str): # Fonction pour formater la date en français
        mois_fr = {1: "janvier", 2: "février", 3: "mars", 4: "avril", 5: "mai", 6: "juin",7: "juillet", 8: "août", 9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"} 
        jours_fr = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi", 5: "samedi", 6: "dimanche"}
        date_format = "%Y-%m-%d %H:%M"
        dateFrom = datetime.strptime(date_str, date_format) # On convertit la date en objet datetime
        jour = jours_fr[dateFrom.weekday()] # On récupère le jour de la semaine
        mois = mois_fr[dateFrom.month] # On récupère le mois
        return dateFrom.strftime(f"{jour} %d {mois} %Y à %H:%M") # On retourne la date formatée en français

    def delete_selected(self): # Méthode pour supprimer les évènements sélectionnés
        selected_index = self.listbox.curselection() # On récupère l'index des évènements sélectionnés dans la liste
        if not selected_index: # Si aucun évènement n'est sélectionné, on affiche un message d'erreur
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins un évènement à supprimer.")
            return
        selected_events = [self.listbox.get(index) for index in selected_index] # On récupère les évènements sélectionnés
        event_ids = [event.split(" - ")[0][2:] for event in selected_events] # On récupère les identifiants des évènements sélectionnés
        confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer les évènements sélectionnés : {', '.join(selected_events)} ?")
        if confirmation:
            success, message = self.db.delete_events(event_ids) # On supprime les évènements sélectionnés
            if success : # Si la suppression est un succès, on affiche un message de succès et on recharge les évènements
                messagebox.showinfo("Succès", message)
                self.load_events()
            else:
                messagebox.showerror("Erreur", message)
