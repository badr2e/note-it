"""Ce fichier est le point d'entrée de l'application. Il permet de lancer l'application Note-it.
On crée une instance de la classe DatabaseHandler, qui permet de gérer la base de données.
On crée ensuite les tables de la base de données, si elles n'existent pas déjà.
On crée une instance de la classe HomePage, qui est la page d'accueil de l'application.
On lance la boucle principale de l'application avec la méthode mainloop() de tkinter qui va permettre d'afficher l'interface graphique et d'écouter les événements.
Enfin, on ferme la connexion à la base de données à la fin de l'utilisation de l'application pour éviter les fuites de mémoire et libérer les ressources utilisées."""


#----------------Importation des modules----------------

from controllers.controller import HomePage
from models.database import DatabaseHandler

#----------------Fonction principale----------------


def main():
    db = DatabaseHandler("note-it.db")
    HomePage(db).mainloop()
    db.close_connection()

if __name__ == "__main__":
    main()