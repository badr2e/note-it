"""Ce fichier contient la classe AddEventPage qui est une interface graphique qui permet à l'utilisateur d'ajouter un évènement à son agenda."""


#----------------Importation des modules----------------


import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry


#----------------Classe AddEventPage----------------


class AddEventPage(tk.Toplevel):
    def __init__(self, master, db, user): # Constructeur de la classe AddEventPage
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

        label_title = tk.Label(self, text="Ajouter un évènement", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        label_title.pack(pady=(20, 10))

        #---------Frame Container Principal---------#
        frame_container = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_container.pack(expand=True, fill='both', padx=(75), pady=(0,20))

        # Le titre
        label_title = tk.Label(frame_container, text="Titre", bg="white", font=("Arial", 15))
        label_title.pack(fill='x', pady=(30,0))
        self.entry_title = tk.Entry(frame_container, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_title.pack(pady=(0,5), padx=50, fill='x')

        # La description
        label_description= tk.Label(frame_container, text="Description", bg="white", font=("Arial", 15))
        label_description.pack(fill='x')
        self.entry_description = tk.Entry(frame_container, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_description.pack(pady=(0,5), padx=50, fill='x')

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
        btn_register.pack(pady=(175,0))
    
    def add_event(self):
        # On récupère les informations saisies par l'utilisateur
        title = self.entry_title.get()
        description = self.entry_description.get()
        dateFrom = self.entry_dateFrom.get_date()
        timeFrom = self.entry_timeFrom.get()
        dateTo = self.entry_dateTo.get_date()
        timeTo = self.entry_timeTo.get()
        
        # On concatène la date et l'heure pour avoir un format complet
        dateTimeFrom = f"{dateFrom} {timeFrom}"
        dateTimeTo = f"{dateTo} {timeTo}"

        success, message = self.db.add_event(self.user, title, description, dateTimeFrom, dateTimeTo) # On ajoute l'évènement à la base de données

        if success : # Si l'ajout a réussi, on affiche un message de succès
            messagebox.showinfo("Succès", message)
        else:
            messagebox.showerror("Erreur", message)