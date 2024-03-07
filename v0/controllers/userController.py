"""Ce fichier contient le contrôleur de l'utilisateur. Il permet de gérer les actions de l'utilisateur une fois qu'il est connecté.
On affiche dans un premier temps la vue du menu principal de l'utilisateur, qui lui permet de choisir entre afficher ses événements, ajouter un événement, supprimer un événement ou se déconnecter.
"""

#----------------Importation des modules----------------


# Importation de la vue du menu principal de l'utilisateur
from views.userViews.mainMenuUserView import mainMenuUserView

# Importation des vues qui gère l'affichage des événements
from views.userViews.displayEventsMenuView import displayEventsMenuView
from views.userViews.displayAllEventsView import displayAllEventsView
from views.userViews.displayNext7DaysEventsView import displayNext7DaysEventsView
from views.userViews.displayEventsBetweenDatesView import getDisplayEventsBetweenDatesView, displayEventsBetweenDatesView

# Importation des vues qui gère l'ajout et la suppression d'événements
from views.userViews.addEventView import addEventView
from views.userViews.deleteEventsView import deleteEventsView


#----------------Fonctions----------------


def mainMenuUser(user, database): # Fonction qui permet d'afficher le menu principal de l'utilisateur
    logged_in = True # On initialise la variable logged_in à True pour que l'utilisateur soit connecté
    print(f"Bienvenue {user[3]} !")
    while logged_in:
        choice = mainMenuUserView() # On affiche la vue du menu principal de l'utilisateur et on récupère le choix de l'utilisateur
        if choice == "1":
            displayEventsMenu(user, database)
        elif choice == "2":
            addEvent(user, database)
        elif choice == "3":
            deleteEvents(user, database)
        elif choice == "4":
            print("À plus tard sur Note it !\n")
            logged_in = False # Si l'utilisateur choisit de se déconnecter, on passe la variable logged_in à False pour qu'il ne soit plus connecté
        else:
            print("Option invalide. Veuillez réessayer.\n")

def displayEventsMenu(user, database): # Fonction qui permet d'afficher le menu pour afficher les événements
    choice = displayEventsMenuView() # On affiche la vue du menu pour afficher les événements et on récupère le choix de l'utilisateur
    if choice == "1":
        displayAllEvents(user, database)
    elif choice == "2":
        displayNext7DaysEvents(user, database)
    elif choice == "3":
        displayEventsBetweenDates(user, database)
    elif choice == "4":
        pass
    else:
        print("Option invalide. Veuillez réessayer.")

def displayAllEvents(user, database): # Fonction qui permet d'afficher tous les événements
    events = database.get_all_events(user)
    displayAllEventsView(events)

def displayNext7DaysEvents(user, database):	# Fonction qui permet d'afficher les événements des 7 prochains jours
    events = database.get_next_7_days_events(user)
    displayNext7DaysEventsView(events)

def displayEventsBetweenDates(user,database): # Fonction qui permet d'afficher les événements entre deux dates
    date1, date2 = getDisplayEventsBetweenDatesView()
    events = database.get_events_between_dates(user, date1, date2)
    displayEventsBetweenDatesView(events,date1,date2)

def addEvent(user,database): # Fonction qui permet d'ajouter un événement
    title, description, dateFrom, dateTo = addEventView() # On affiche la vue pour ajouter un événement et on récupère les informations entrées par l'utilisateur
    if database.add_event(user, title, description, dateFrom, dateTo):
        print("Événement ajouté avec succès !\n")
    else:
        print("L'ajout de l'événement a échoué.\n")

def deleteEvents(user,database): # Fonction qui permet de supprimer un événement
    displayAllEvents(user,database) # On affiche tous les événements pour que l'utilisateur puisse choisir l'événement à supprimer
    events_ids = deleteEventsView() # On affiche la vue pour supprimer un événement et on récupère les identifiants des événements à supprimer
    if database.delete_events(events_ids) :
        print("Événement(s) supprimé(s) avec succès !\n")
    else:
        print("La suppression de l'événement a échoué.\n")