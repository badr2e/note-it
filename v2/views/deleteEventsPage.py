"""Ce fichier est la page de suppression d'évènements de l'application. Elle permet à l'utilisateur de supprimer des évènements."""


#----------------Importation des modules----------------


import tkinter as tk
from tkinter import messagebox
from datetime import datetime


#----------------Classe DeleteEventsPage----------------


class DeleteEventsPage(tk.Frame): # On initialise la classe DeleteEventsPage.
    def __init__(self, db, user):
        tk.Frame.__init__(self)
        self.db = db
        self.user = user
        self.configure(bg="#0053f4")
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self, text="Supprimer des évènements", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        title.pack(pady=(20))

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
        categories = {category[0]: (category[1], category[2]) for category in self.db.get_user_categories_and_colors(self.user)}  # Dictionnaire de catégories {idCategory: (nameCategory, hexColor)}
        
        for event in events:
            idEvent, idUser, title, description, dateFrom, dateTo, category_id = event
            category_name, category_color = categories.get(category_id, ("Inconnue", "#FFFFFF"))  # Récupérer le nom et la couleur de la catégorie, avec une valeur par défaut si la catégorie n'est pas trouvée
            formatted_dateFrom = DeleteEventsPage.format_date_french(dateFrom) # On formate la date de début en français
            formatted_dateTo = DeleteEventsPage.format_date_french(dateTo) # On formate la date de fin en français
            event_info = f"N°{idEvent} - {title} - {description} - Du {formatted_dateFrom} au {formatted_dateTo} - Catégorie: {category_name}"  # Informations de l'événement avec le nom de la catégorie
            self.listbox.insert(tk.END, event_info) # On insère les évènements dans la liste
            self.listbox.itemconfig(tk.END, {'bg': category_color, 'fg': 'white'})  # Appliquer la couleur de la catégorie en fond

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