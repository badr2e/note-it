from views.userViews.displayAllEventsView import display_events

def displayNext7DaysEventsView(events):
    if events:
        print("==Tous les évènements des 7 prochains jours==")
        display_events(events)
        print()
    else:
        print("Rien de prévu pour les 7 prochains jours !\n")