"""Ce module contient la classe ShowEventsPage qui permet d'afficher les évènements de l'utilisateur grâce à un filtre de dates."""


#----------------Importation des modules----------------


from datetime import datetime
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox


#----------------Classe ShowEventsPage----------------


class ShowEventsPage(tk.Toplevel):
    def __init__(self, master, db, user): # Constructeur de la classe ShowEventsPage
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

        # Titre
        label_title = tk.Label(self, text="Afficher les évènements", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        label_title.pack(pady=(20, 10))

        # Frame qui va contenir les endroits liées aux dates pour filtrer les évènements
        frame_dates = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_dates.pack(padx=30, pady=10, fill='both')

        # Les labels et les champs pour la date et l'heure de début
        label_from = tk.Label(frame_dates, text="Date de début :", font=("Arial", 14), bg="white")
        label_from.grid(row=0, column=0, padx=(0, 10), pady=10)
        self.entry_dateFrom = DateEntry(frame_dates, width=12, background='#0053f4', foreground='white', borderwidth=2)
        self.entry_dateFrom.grid(row=0, column=1)
        label_timeFrom = tk.Label(frame_dates, text="Heure de début :", font=("Arial", 14), bg="white")
        label_timeFrom.grid(row=0, column=2, padx=(20, 10), pady=10)
        self.entry_timeFrom = tk.Entry(frame_dates, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_timeFrom.grid(row=0, column=3)

        # Les labels et les champs pour la date et l'heure de fin
        label_to = tk.Label(frame_dates, text="Date de fin :", font=("Arial", 14), bg="white")
        label_to.grid(row=1, column=0, padx=(0, 10), pady=10)
        self.entry_dateTo = DateEntry(frame_dates, width=12, background='#0053f4', foreground='white', borderwidth=2)
        self.entry_dateTo.grid(row=1, column=1)
        label_timeTo = tk.Label(frame_dates, text="Heure de fin :", font=("Arial", 14), bg="white")
        label_timeTo.grid(row=1, column=2, padx=(20, 10), pady=10)
        self.entry_timeTo = tk.Entry(frame_dates, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.entry_timeTo.grid(row=1, column=3)

        # Bouton pour filtrer les évènements
        btn_filter = tk.Button(frame_dates, text="Filtrer", command=self.filter_events, bg="#0053f4", fg="white", font=("Arial", 15))
        btn_filter.grid(row=0, column=4, padx=(50, 0), rowspan=2)

        # Frame qui va contenir la liste des évènements
        frame_events = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_events.pack(expand=True, fill='both', padx=30, pady=(0, 20))

        # Ajout d'une barre de défilement à droite et qui se remplit verticalement
        scrollbar = tk.Scrollbar(frame_events, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Création d'une liste pour afficher les évènements
        self.listbox = tk.Listbox(frame_events, yscrollcommand=scrollbar.set, font=("Arial", 11), bg="white", fg="black", selectbackground="white", selectforeground="black")
        self.listbox.pack(expand=True, fill='both')

        scrollbar.config(command=self.listbox.yview) # Configuration de la barre de défilement pour se synchroniser avec la liste

        self.load_initial_dates() # Charger les dates initiales

    def load_initial_dates(self): # Méthode pour charger les dates initiales
        self.entry_timeFrom.insert(0, "00:00") # Dans le cas où l'utilisateur n'a pas d'évènements, on initialise les dates à minuit et 23h59
        self.entry_timeTo.insert(0, "23:59")
        events = self.db.get_all_events(self.user)
        if events:
            # Pour afficher tous les évènements, on initialise les champs par les dates du premier et du dernier évènement de l'utilisateur
            self.entry_timeFrom.delete(0, tk.END)
            self.entry_timeTo.delete(0, tk.END)
            first_event = min(events, key=lambda x: datetime.strptime(x[4], "%Y-%m-%d %H:%M")) # On récupère le premier évènement (min) (car la liste a été trié en ordre croissant par la base de données)
            self.entry_dateFrom.set_date(datetime.strptime(first_event[4], "%Y-%m-%d %H:%M").date()) # On récupère la date de début du premier évènement
            self.entry_timeFrom.insert(0, datetime.strptime(first_event[4], "%Y-%m-%d %H:%M").strftime("%H:%M")) # On récupère l'heure de début du premier évènement

            last_event = max(events, key=lambda x: datetime.strptime(x[5], "%Y-%m-%d %H:%M")) # On récupère le dernier évènement (max) (car la liste a été trié en ordre croissant par la base de données)
            self.entry_dateTo.set_date(datetime.strptime(last_event[5], "%Y-%m-%d %H:%M").date()) # On récupère la date de fin du dernier évènement
            self.entry_timeTo.insert(0, datetime.strptime(last_event[5], "%Y-%m-%d %H:%M").strftime("%H:%M")) # On récupère l'heure de fin du dernier évènement

        self.filter_events() # On filtre les évènements entre les deux dates

    def filter_events(self):
        date_from = self.entry_dateFrom.get_date()
        time_from = self.entry_timeFrom.get()
        date_to = self.entry_dateTo.get_date()
        time_to = self.entry_timeTo.get()

        # Concaténation des dates
        dateTimeFrom = f"{date_from} {time_from}"
        dateTimeTo = f"{date_to} {time_to}"

        events, message = self.db.get_events_between_dates(self.user, dateTimeFrom, dateTimeTo) # On récupère les évènements entre les deux dates
        
        self.listbox.delete(0, tk.END) # On efface la liste actuelle pour afficher les nouveaux évènements

        if not events :
            messagebox.showwarning("Erreur", message)
        else:
            for event in events:
                idEvent, title, description, dateFrom, dateTo = event[0], *event[2:6]
                formatted_dateFrom = ShowEventsPage.format_date_french(dateFrom) # On formate la date de début en français
                formatted_dateTo = ShowEventsPage.format_date_french(dateTo) # On formate la date de fin en français
                self.listbox.insert(tk.END, f"N°{idEvent} - {title} - {description} - Du {formatted_dateFrom} au {formatted_dateTo}") # On insère les évènements dans la liste

    @staticmethod
    def format_date_french(date_str): # Fonction pour formater la date en français
        mois_fr = {1: "janvier", 2: "février", 3: "mars", 4: "avril", 5: "mai", 6: "juin",7: "juillet", 8: "août", 9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"} 
        jours_fr = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi", 5: "samedi", 6: "dimanche"}
        date_format = "%Y-%m-%d %H:%M"
        dateFrom = datetime.strptime(date_str, date_format) # On convertit la date en objet datetime
        jour = jours_fr[dateFrom.weekday()] # On récupère le jour de la semaine
        mois = mois_fr[dateFrom.month] # On récupère le mois
        return dateFrom.strftime(f"{jour} %d {mois} %Y à %H:%M") # On retourne la date formatée en français