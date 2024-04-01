"""Ce fichier est la page d'ajout d'évènement de l'application. Elle permet à l'utilisateur d'ajouter un évènement."""


#----------------Importation des modules----------------


import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk


#----------------Classe AddEventPage----------------


class AddEventPage(tk.Frame): # On initialise la classe AddEventPage.
    def __init__(self, db, user):
        tk.Frame.__init__(self)
        self.db = db
        self.user = user
        self.configure(bg="#0053f4")
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self, text="Ajouter un évènement", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        title.pack(pady=(15))
        
        frame_container = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_container.pack(expand=True, fill='both', padx=(75), pady=(0,20))

        # Le titre
        label_title = tk.Label(frame_container, text="Titre", bg="white", font=("Arial", 15))
        label_title.pack(fill='x', pady=(5,0))
        self.entry_title = tk.Entry(frame_container, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_title.pack(pady=(0,5), padx=50, fill='x')

        # La description
        label_description= tk.Label(frame_container, text="Description", bg="white", font=("Arial", 15))
        label_description.pack(fill='x')
        self.entry_description = tk.Entry(frame_container, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_description.pack(pady=(0,5), padx=50, fill='x')

        # La catégorie
        label_category = tk.Label(frame_container, text="Catégorie", bg="white", font=("Arial", 15))
        label_category.pack(fill='x')
        self.category_combobox = ttk.Combobox(frame_container, state="readonly")
        self.category_combobox.pack(pady=(0, 5), padx=50, fill='x')
        self.update_category_combobox()  # On appelle cette méthode pour mettre à jour les catégories disponibles

        # La date et l'heure de début (on crée une frame spéciale)
        frame_datetimeFrom = tk.Frame(frame_container, bg="white")
        frame_datetimeFrom.pack(side="left", expand=True, fill='both', padx=(50,0))
        label_dateFrom = tk.Label(frame_datetimeFrom, text="Date de début", bg="white", font=("Arial", 15))
        label_dateFrom.pack(pady=(17,0))
        self.entry_dateFrom = DateEntry(frame_datetimeFrom, width=12, background='#0053f4', foreground='white', borderwidth=2)
        self.entry_dateFrom.pack()
        label_timeFrom = tk.Label(frame_datetimeFrom, text="Heure de début", bg="white", font=("Arial", 15))
        label_timeFrom.pack(pady=(17,0))
        self.entry_timeFrom = tk.Entry(frame_datetimeFrom, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_timeFrom.pack()

        # La date et l'heure de fin (on crée une frame spéciale)
        frame_datetimeTo = tk.Frame(frame_container, bg="white")
        frame_datetimeTo.pack(side="right", expand=True, fill='both', padx=(0,50))
        label_dateTo = tk.Label(frame_datetimeTo, text="Date de fin", bg="white", font=("Arial", 15))
        label_dateTo.pack(pady=(17,0))
        self.entry_dateTo = DateEntry(frame_datetimeTo, width=12, background='#0053f4', foreground='white', borderwidth=2)
        self.entry_dateTo.pack()
        label_timeTo = tk.Label(frame_datetimeTo, text="Heure de fin", bg="white", font=("Arial", 15))
        label_timeTo.pack(pady=(17,0))
        self.entry_timeTo = tk.Entry(frame_datetimeTo, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_timeTo.pack()

        self.entry_timeFrom.insert(0, "00:00")  # Définir l'heure de début à 00:00
        self.entry_timeTo.insert(0, "23:59")  # Définir l'heure de fin à 00:00

        btn_register = tk.Button(frame_container, text="Ajouter", command=self.add_event, bg="#0053f4", fg="white", font=("Arial", 15)) # Bouton pour ajouter l'évènement
        btn_register.pack(pady=(150,0))

    def update_category_combobox(self): # Met à jour la liste des catégories
        categories = self.db.get_categories(self.user)
        self.category_combobox['values'] = [(category[2]) for category in categories] # On récupère les noms des catégories
        self.category_combobox.set("Sélectionner une catégorie")
    
    def add_event(self):
        title = self.entry_title.get()
        if not title.strip():
            messagebox.showerror("Erreur", "Un titre est requis pour l'événement.")
            return
        
        description = self.entry_description.get()
        category_index = self.category_combobox.current()
        dateFrom = self.entry_dateFrom.get_date()
        timeFrom = self.entry_timeFrom.get()
        dateTo = self.entry_dateTo.get_date()
        timeTo = self.entry_timeTo.get()
        if category_index == -1:
            messagebox.showerror("Erreur", "Veuillez sélectionner une catégorie.")
            return
        # On concatène les dates et les heures pour obtenir la date et l'heure de début et de fin
        dateTimeFrom = f"{dateFrom} {timeFrom}"
        dateTimeTo = f"{dateTo} {timeTo}"

        success, message = self.db.add_event(self.user, title, description, dateTimeFrom, dateTimeTo, category_index+1)

        if success:
            messagebox.showinfo("Succès", message)
        else:
            messagebox.showerror("Erreur", message)
