from views.userViews.displayAllEventsView import display_events, format_date_french

def getDisplayEventsBetweenDatesView():
    date1 = input("Entrez la date de début (format YYYY-MM-DD HH:MM) : ")
    date2 = input("Entrez la date de fin (format YYYY-MM-DD HH:MM) : ")
    print()
    
    return date1, date2

def displayEventsBetweenDatesView(events,date1,date2):
    if events:
        print(f"==Tous les évènements entre le {format_date_french(date1)} et le {format_date_french(date1)}==")
        display_events(events)
        print()
    else:
        print("Aucun événement trouvé pour cette période.\n")