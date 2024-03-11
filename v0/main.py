"""Ce fichier est le point d'entrée de l'application. Il permet de lancer l'application Note-it.
On crée une instance de la classe DatabaseHandler, qui permet de gérer la base de données.
On crée ensuite les tables de la base de données, si elles n'existent pas déjà.
On appelle ensuite la fonction start du module homeController, qui permet de lancer l'application.
Enfin, on ferme la connexion à la base de données à la fin de l'utilisation de l'application pour éviter les fuites de mémoire et libérer les ressources utilisées."""


#----------------Importation des modules----------------


from models.database import DatabaseHandler # Importation de la classe DatabaseHandler du module database
from controllers import homeController # Importation du module homeController


#----------------Fonction principale----------------


def main():
    database = DatabaseHandler("noteit.db")
    database.create_tables()
    homeController.start(database)
    database.close_connection()


#----------------Appel de la fonction principale----------------
if __name__ == "__main__":
    main()