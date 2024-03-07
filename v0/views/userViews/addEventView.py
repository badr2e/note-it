def addEventView():
    print("===Ajouter un événement===")
    title = input("Titre de l'événement : ")
    description = input("Description de l'événement (optionnel) : ")
    dateFrom = input("Date de début de l'événement (format YYYY-MM-DD HH:MM) : ")
    dateTo = input("Date de fin de l'événement (format YYYY-MM-DD HH:MM) : ")
    
    return title, description, dateFrom, dateTo