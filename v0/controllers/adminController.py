"""Ce fichier contient le contrôleur de l'administrateur. Il permet de gérer les actions de l'administrateur une fois qu'il est connecté.
On affiche dans un premier temps la vue du menu principal de l'administrateur, qui lui permet de choisir entre afficher le nombre de comptes, supprimer un compte ou se déconnecter."""

#----------------Importation des modules----------------


# Importation de la vue du menu principal de l'administrateur
from views.adminViews.mainMenuAdminView import mainMenuAdminView

# Importation de la vue qui gère l'affichage du nombre de comptes
from views.adminViews.deleteAccountView import deleteAccountView

# Importation de la vue qui gère l'affichage du nombre de comptes
from views.adminViews.displayNumberAccountsView import displayNumberAccountsView

#----------------Fonctions----------------


def mainMenuAdmin(admin,database): # Fonction qui permet d'afficher le menu principal de l'administrateur
    logged_in = True # On initialise la variable logged_in à True pour que l'administrateur soit connecté
    print(f"Bienvenue {admin[3]} !")
    while logged_in:
        choice = mainMenuAdminView() # On affiche la vue du menu principal de l'administrateur et on récupère le choix de l'administrateur
        if choice == "1":
            displayNumberAccounts(database)
        elif choice == "2":
            deleteAccount(database,admin[0])
        elif choice == "3":
            print("À plus tard sur Note it !\n")
            logged_in = False # Si l'administrateur choisit de se déconnecter, on passe la variable logged_in à False pour qu'il ne soit plus connecté
        else:
            print("Option invalide. Veuillez réessayer.\n")

def displayNumberAccounts(database): # Fonction qui permet d'afficher le nombre de comptes
    nbrAccounts = database.get_number_accounts()
    displayNumberAccountsView(nbrAccounts)

def deleteAccount(database, currentUserId): # Fonction qui permet de supprimer un compte sauf celui de l'administrateur
    accounts = database.get_all_accounts() # On récupère tous les comptes
    if accounts: # Si il y a des comptes, on les affiche et on demande à l'administrateur de choisir le compte à supprimer
        print("==Tous les comptes==")
        for account in accounts:
            print(f"N°{account[0]} - {account[2]} - {account[3]}")
        print()
        idUser = deleteAccountView()
        if database.delete_account(idUser, currentUserId):
            print("Compte supprimé avec succès !\n")
        else:
            print("Erreur lors de la suppression du compte ou nom d'utilisateur incorrect !\n")
    else:
        print("Il n'y a aucun compte à supprimer.\n")