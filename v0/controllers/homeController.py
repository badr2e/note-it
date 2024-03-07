"""Ce fichier est le point d'entrée de l'application. Il permet de lancer l'application NoteIt en affichant la première vue dans la fonction start.
La première vue, qui est la page d'accueil, permet à l'utilisateur de choisir entre s'inscrire, se connecter, réinitialiser son mot de passe ou quitter l'application.
En fonction du choix de l'utilisateur, on appelle les fonctions correspondantes et on affiche les vues correspondantes.
Par exemple si l'utilisateur choisit de s'inscrire, on appelle la fonction register du module homeController, qui permet de s'inscrire."""


#----------------Importation des modules----------------


# Importation des vues
from views.homeViews.homePageView import homePageView
from views.homeViews.registerView import registerView
from views.homeViews.loginView import loginView
from views.homeViews.passwordForgotView import passwordForgotView

# Importation des contrôleurs
from controllers.userController import mainMenuUser
from controllers.adminController import mainMenuAdmin


#----------------Fonctions----------------


def start(database): # Fonction qui permet de lancer l'application
    while True:
        choice = homePageView() # On affiche la page d'accueil et on récupère le choix de l'utilisateur
        if choice == "1":
            register(database)
        elif choice == "2":
            login(database)
        elif choice == "3":
            password_forgot(database)
        elif choice == "4":
            print("À plus tard sur Note it !\n")
            break
        else:
            print("Option invalide. Veuillez réessayer.\n")

def register(database): # Fonction qui permet de s'inscrire
    email, username, password = registerView() # On affiche la page d'incription et on récupère les informations entrées par l'utilisateur
    if database.register(email, username, password):
        print("Compte créé avec succès !\n")
    else:
        print("La création du compte a échoué.\n")

def login(database): # Fonction qui permet de se connecter
    username, password = loginView() # On affiche la page de connexion et on récupère les informations entrées par l'utilisateur
    account = database.login(username, password)
    if account:
        print("Connexion réussie !\n")
        if account[1] == 1: # Si l'utilisateur est un administrateur
            mainMenuAdmin(account, database)
        else:
            mainMenuUser(account, database)
    else:
        print("Nom d'utilisateur ou mot de passe incorrect !\n")

def password_forgot(database): # Fonction qui permet de réinitialiser son mot de passe
    email, username = passwordForgotView() # On affiche la page de réinitialisation de mot de passe et on récupère les informations entrées par l'utilisateur
    account = database.is_account(email, username) # On vérifie si un compte existe avec ces informations
    if account:
        newPassword = input("Entrez votre nouveau mot de passe : ")
        if database.password_forgot(account, newPassword):
            print("Mot de passe changé avec succès !\n")
        else:
            print("Erreur lors du changement de mot de passe.\n")
    else:
        print("Aucun compte trouvé avec cet email et ce nom d'utilisateur.\n")