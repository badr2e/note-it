from datetime import datetime

def displayAllEventsView(events):
    if events:
        print("==Tous les événements==")
        display_events(events)
        print()
    else:
        print("Rien de prévu !\n")

def format_date_french(date_str): # Fonction pour formater la date en français
    mois_fr = {1: "janvier", 2: "février", 3: "mars", 4: "avril", 5: "mai", 6: "juin",7: "juillet", 8: "août", 9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"} 
    jours_fr = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi", 5: "samedi", 6: "dimanche"}
    date_format = "%Y-%m-%d %H:%M"
    dateFrom = datetime.strptime(date_str, date_format) # On convertit la date en objet datetime
    jour = jours_fr[dateFrom.weekday()] # On récupère le jour de la semaine
    mois = mois_fr[dateFrom.month] # On récupère le mois
    return dateFrom.strftime(f"{jour} %d {mois} %Y à %H:%M") # On retourne la date formatée en français

def display_events(events):
    for event in events:
        idEvent, title, description, dateFrom, dateTo = event[0], *event[2:6]
        formatted_dateFrom = format_date_french(dateFrom)
        formatted_dateTo = format_date_french(dateTo)
        print(f"N°{idEvent} - {title} - {description} - Du {formatted_dateFrom} au {formatted_dateTo}")