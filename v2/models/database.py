"""Ce fichier contient la classe DatabaseHandler qui gère la base de données SQLite3 de notre application.
Elle contient des méthodes pour créer les tables, insérer des données, récupérer des données, supprimer des données, etc."""


#----------------Importation des modules----------------


import sqlite3 # Module pour interagir avec la base de données SQLite3
import os # Module pour interagir avec le système d'exploitation pour récupérer le chemin absolu du fichier
import hashlib # Module pour gérer le hachage des mots de passe
import re # Module pour gérer le bon format des emails grâce aux expressions régulières 
from datetime import datetime # Module pour gérer les dates et heures

class DatabaseHandler:


    #----------------Initialisation de la base de données----------------


    def __init__(self, db_file): # Constructeur de la classe
            self.connection = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{db_file}") # Connexion à la base de données
            self.cursor = self.connection.cursor() # Création d'un objet curseur pour exécuter des requêtes SQL
            self.connection.row_factory = sqlite3.Row # Récupération des données sous forme de dictionnaire
            self.create_tables() # Appel de la méthode pour créer les tables de la base de données

    def create_tables(self): # Méthode pour créer les tables de la base de données
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                                    idUser INTEGER PRIMARY KEY,
                                    isAdmin INTEGER NOT NULL,
                                    email TEXT UNIQUE NOT NULL,
                                    username TEXT UNIQUE NOT NULL,
                                    password TEXT NOT NULL);''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Color (
                                    idColor INTEGER PRIMARY KEY,
                                    nameColor TEXT NOT NULL,
                                    hexColor TEXT NOT NULL);''')
            
            # Liste des couleurs à insérer
            colors = [("Azur", "#3A4162"), ("Cyan", "#336E83"),("Sable", "#FFF5D0"),("Or", "#F7CE72"),("Vermillon", "#F77269"),("Émeraude", "#4dbf78")]
            for color in colors :
                self.cursor.execute("SELECT idColor FROM Color WHERE nameColor=? OR hexColor=?", (color[0], color[1]))
                existing_color = self.cursor.fetchone()
                if existing_color:
                    continue
                self.cursor.execute('''INSERT INTO Color (nameColor, hexColor) 
                                    VALUES (?, ?)''', color)
                
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Category (
                                    idCategory INTEGER PRIMARY KEY,
                                    idUser INTEGER NOT NULL,
                                    nameCategory TEXT NOT NULL,
                                    idColor INTEGER NOT NULL,
                                    FOREIGN KEY (idColor) REFERENCES Color (idColor),
                                    FOREIGN KEY (idUser) REFERENCES User (idUser));''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Event (
                                    idEvent INTEGER PRIMARY KEY,
                                    idUser INTEGER NOT NULL,
                                    title TEXT NOT NULL,
                                    description TEXT,
                                    dateFrom TEXT NOT NULL,
                                    dateTo TEXT NOT NULL,
                                    idCategory INTEGER,
                                    FOREIGN KEY (idUser) REFERENCES User (idUser),
                                    FOREIGN KEY (idCategory) REFERENCES Category (idCategory));''')
            self.connection.commit()
        except Exception as e:
            print("Erreur lors de la création des tables:", e)
            self.connection.rollback()

    def close_connection(self): # Méthode pour fermer la connexion à la base de données
        self.connection.close()


    #----------------Méthodes liées à la page d'accueil----------------
        

    def register(self, email, username, password): # Méthode pour inscrire un utilisateur, renvoie True si l'inscription a réussi, False sinon
        if not email or not username or not password:
            return False, "Tous les champs sont requis."
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): # Vérifier si l'email est au bon format
            return False, "Format d'email invalide"
        try:
            self.cursor.execute("SELECT * FROM User WHERE email=?", (email,)) # Vérifier si l'email est déjà utilisé
            if self.cursor.fetchone():
                return False, "Cet email est déjà utilisé"
            self.cursor.execute("SELECT * FROM User WHERE username=?", (username,)) # Vérifier si l'username est déjà utilisé
            if self.cursor.fetchone():
                return False, "Ce nom d'utilisateur est déjà utilisé"
            self.cursor.execute("SELECT COUNT(*) FROM User WHERE isAdmin=1") # S'il n'y a pas d'administrateur dans la base de données, le premier utilisateur inscrit sera un administrateur
            admin_count = self.cursor.fetchone()[0]
            if admin_count == 0:
                is_admin = True
            else:
                is_admin = False
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute("INSERT INTO User (email, username, password, isAdmin) VALUES (?, ?, ?, ?)",(email, username, hashed_password, is_admin)) # Hachage du mot de passe et insertion des données dans la base de données
            self.connection.commit() # Validation de l'exécution de la transaction
            return True, "Inscription réussie !"
        except Exception as e:
            self.connection.rollback() # Annulation de l'exécution de la transaction (on revient avant l'insertion des données)
            return False, e

    def login(self, username, password): # Méthode pour connecter un utilisateur, renvoie les données de l'utilisateur si la connexion a réussi, None sinon
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest() 
            self.cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, hashed_password))
            account = self.cursor.fetchone()
            if account:
                return account, "Connexion réussie !"
            else:
                return None, "Nom d'utilisateur ou mot de passe incorrect."
        except Exception as e:
            return None, e


    #----------------Méthodes liées au menu principal utilisateur et aux évènements----------------
        
    def get_colors(self): 
        try:
            self.cursor.execute("SELECT * FROM Color")
            colors = self.cursor.fetchall()
            return colors
        except Exception as e:
            return None
        
    def get_categories(self,user):
        try:
            self.cursor.execute("SELECT * FROM Category WHERE idUser=?", (user[0],))
            categories = self.cursor.fetchall()
            return categories
        except Exception as e:
            return None

    def get_user_categories_and_colors(self, user):
        try:
            self.cursor.execute("SELECT Category.idCategory, Category.nameCategory, Color.hexColor FROM Category JOIN Color ON Category.idColor = Color.idColor WHERE idUser=?", (user[0],))
            categories = self.cursor.fetchall()
            return categories
        except Exception as e:
            return None

    def add_category(self, user, name, color_id):
        try:
            self.cursor.execute("INSERT INTO Category (idUser, nameCategory, idColor) VALUES (?, ?, ?)", (user[0], name, color_id))
            self.connection.commit()
            return True, "Catégorie ajoutée avec succès !"
        except Exception as e:
            self.connection.rollback()
            return False, str(e)

    @staticmethod
    def validate_dates(date1, date2): # Méthode de classe pour valider les dates de début et de fin d'un événement
        date_format = "%Y-%m-%d %H:%M"
        try:
            date1 = datetime.strptime(date1, date_format)
            date2 = datetime.strptime(date2, date_format)
            if date1 >= date2:
                return False, "La date de début doit être antérieure à la date de fin."
            return True, ""
        except ValueError:
            return False, "Format d'heure invalide. Utilisez le format HH:MM."
        
    def add_event(self, user, title, description, date1, date2, category): # Méthode pour ajouter un événement, renvoie True si l'ajout a réussi, False sinon
        valid, message = DatabaseHandler.validate_dates(date1, date2) # Vérifier si les dates sont au bon format
        if not valid:
            return False, message
        try:
            self.cursor.execute("INSERT INTO Event (idUser, title, description, dateFrom, dateTo, idCategory) VALUES (?, ?, ?, ?, ?, ?)",(user[0], title, description, date1, date2, category))
            self.connection.commit()
            return True, "Évènement ajouté avec succès !"
        except Exception as e:
            self.connection.rollback()
            return False, e

    def get_all_events(self, user):
        self.cursor.execute("SELECT * FROM Event WHERE idUser=? ORDER BY dateFrom ASC", (user[0],))
        events = self.cursor.fetchall()
        return events

    def get_events_between_dates(self, user, date1, date2): # Méthode pour récupérer les événements d'un utilisateur entre deux dates
        valid, message = DatabaseHandler.validate_dates(date1, date2) # Vérifier si les dates sont au bon format
        if not valid:
            return None, message
        try:
            self.cursor.execute("SELECT * FROM Event WHERE idUser = ? AND dateFrom >= ? AND dateTo <= ? ORDER BY dateTo ASC", (user[0], date1, date2))
            events = self.cursor.fetchall()
            return events, "Aucun évènement trouvé."
        except ValueError:
            return None, "Veuillez sélectionner une plage de dates différente."
    
    def delete_events(self, event_ids): 
        try:
            event_ids = [int(id) for id in event_ids]
            placeholders = ",".join("?" * len(event_ids))
            query = "DELETE FROM Event WHERE idEvent IN ({})".format(placeholders)
            self.cursor.execute(query, event_ids)
            self.connection.commit()
            return True, "Évènements supprimés avec succès !"
        except Exception as e:
            return False, e


    #----------------Méthodes liées au menu principal administrateur et à la gestion des comptes----------------
        

    def get_number_accounts(self): # Méthode pour récupérer le nombre de comptes utilisateurs
        self.cursor.execute("SELECT COUNT(*) FROM User")
        return self.cursor.fetchone()[0]

    def get_all_accounts(self): # Méthode pour récupérer tous les comptes utilisateurs
        self.cursor.execute("SELECT * FROM User WHERE isAdmin=0")
        accounts = self.cursor.fetchall()
        return accounts

    def delete_account(self, idUser, currentUserId): # Méthode pour supprimer un compte utilisateur, renvoie True si la suppression a réussi, False sinon
        if idUser == str(currentUserId):
            return False, "Vous ne pouvez pas supprimer votre propre compte."
        try:
            self.cursor.execute("SELECT idEvent FROM Event WHERE idUser=?", (idUser,))
            self.cursor.execute("DELETE FROM Category WHERE idUser=?", (idUser,))
            event_ids = [str(row[0]) for row in self.cursor.fetchall()]
            self.delete_events(",".join(event_ids)) # Supprimer les événements associés à l'utilisateur
            self.cursor.execute("DELETE FROM User WHERE idUser=?", (idUser,)) # Supprimer l'utilisateur
            self.connection.commit()
            return True, "Compte supprimé avec succès !"
        except Exception as e:
            self.connection.rollback()
            return False, e