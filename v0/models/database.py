"""Ce fichier contient la classe DatabaseHandler qui gère la base de données SQLite3 de notre application.
Elle contient des méthodes pour créer les tables, insérer des données, récupérer des données, supprimer des données, etc."""


#----------------Importation des modules----------------


import sqlite3 # Module pour interagir avec la base de données SQLite3
import os # Module pour interagir avec le système d'exploitation pour récupérer le chemin absolu du fichier
import hashlib # Module pour gérer le hachage des mots de passe
import re # Module pour gérer le bon format des emails grâce aux expressions régulières 
from datetime import datetime,timedelta # Module pour gérer les dates et heures

class DatabaseHandler:


    #----------------Initialisation de la base de données----------------


    def __init__(self, db_file): # Constructeur de la classe
            self.connection = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{db_file}") # Connexion à la base de données
            self.cursor = self.connection.cursor() # Création d'un objet curseur pour exécuter des requêtes SQL
            self.connection.row_factory = sqlite3.Row # Récupération des données sous forme de dictionnaire

    def create_tables(self): # Méthode pour créer les tables de la base de données
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                                    idUser INTEGER PRIMARY KEY,
                                    isAdmin INTEGER NOT NULL,
                                    email TEXT UNIQUE NOT NULL,
                                    username TEXT UNIQUE NOT NULL,
                                    password TEXT NOT NULL);''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Event (
                                    idEvent INTEGER PRIMARY KEY,
                                    idUser INTEGER NOT NULL,
                                    title TEXT NOT NULL,
                                    description TEXT,
                                    dateFrom TEXT NOT NULL,
                                    dateTo TEXT NOT NULL,
                                    FOREIGN KEY (idUser) REFERENCES User (idUser));''')
            self.connection.commit()
        except Exception as e:
            print("Erreur lors de la création des tables:", e)
            self.connection.rollback()

    def close_connection(self): # Méthode pour fermer la connexion à la base de données
        self.connection.close()


    #----------------Méthodes liées à la page d'accueil----------------
        

    def register(self, email, username, password): # Méthode pour inscrire un utilisateur, renvoie True si l'inscription a réussi, False sinon
        if not email or not username or not password:
            print("Tous les champs sont requis")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): # Vérifier si l'email est au bon format
            print("Format d'email invalide")
            return False
        try:
            # Vérifier si l'email est déjà utilisé
            self.cursor.execute("SELECT * FROM User WHERE email=?", (email,))
            if self.cursor.fetchone():
                print("Cet email est déjà utilisé")
                return False
            # Vérifier si l'username est déjà utilisé
            self.cursor.execute("SELECT * FROM User WHERE username=?", (username,))
            if self.cursor.fetchone():
                print("Ce nom d'utilisateur est déjà utilisé")
                return False
            # S'il n'y a pas d'administrateur dans la base de données, le premier utilisateur inscrit sera un administrateur
            self.cursor.execute("SELECT COUNT(*) FROM User WHERE isAdmin=1")
            admin_count = self.cursor.fetchone()[0]
            if admin_count == 0:
                is_admin = True
            else:
                is_admin = False
            # Hachage du mot de passe et insertion des données dans la base de données
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute("INSERT INTO User (email, username, password, isAdmin) VALUES (?, ?, ?, ?)",(email, username, hashed_password, is_admin))
            self.connection.commit() # Validation de l'exécution de la transaction
            return True
        except Exception as e:
            print("Erreur lors de l'insertion des données:", e)
            self.connection.rollback() # Annulation de l'exécution de la transaction (on revient avant l'insertion des données)
            return False

    def login(self, username, password): # Méthode pour connecter un utilisateur, renvoie les données de l'utilisateur si la connexion a réussi, None sinon
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest() 
            self.cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, hashed_password))
            account = self.cursor.fetchone()
            if account:
                return account
            else:
                return None
        except Exception as e:
            print("Erreur lors de la récupération des données:", e)
            return None
        
    def is_account(self, email, username): # Méthode pour vérifier si un compte existe déjà
        self.cursor.execute("SELECT * FROM User WHERE email=? AND username=?", (email, username))
        account = self.cursor.fetchone()
        return account
    
    def password_forgot(self, account, newPassword): # Méthode pour réinitialiser le mot de passe d'un utilisateur
        try:
            hashed_password = hashlib.sha256(newPassword.encode()).hexdigest()
            self.cursor.execute("UPDATE User SET password=? WHERE idUser=?", (hashed_password, account[0]))
            self.connection.commit()
            return True
        except Exception as e:
            print("Erreur lors de la mise à jour du mot de passe:", e)
            self.connection.rollback()
            return False


    #----------------Méthodes liées au menu principal utilisateur et aux évènements----------------
        

    @staticmethod
    def validate_dates(date1, date2): # Méthode de classe pour valider les dates de début et de fin d'un événement
        date_format = "%Y-%m-%d %H:%M"
        date1 = datetime.strptime(date1, date_format)
        date2 = datetime.strptime(date2, date_format)
        try:
            if date1 >= date2:
                return False, "La date de début doit être antérieure à la date de fin."
            return True, ""
        except ValueError:
            return False, "Format de date invalide. Utilisez le format YYYY-MM-DD HH:MM."

    def add_event(self, user, title, description, date1, date2): # Méthode pour ajouter un événement, renvoie True si l'ajout a réussi, False sinon
        # Vérifier si les dates sont au bon format
        valid, message = DatabaseHandler.validate_dates(date1, date2)
        if not valid:
            print(message)
            return False
        try:
            if not title.strip(): # Vérifier si le titre est vide
                print("Un titre est requis pour l'événement.")
                return False
            self.cursor.execute("INSERT INTO Event (idUser, title, description, dateFrom, dateTo) VALUES (?, ?, ?, ?, ?)",(user[0], title, description, date1, date2))
            self.connection.commit()
            return True
        except Exception as e:
            print("Erreur lors de l'insertion des données:", e)
            self.connection.rollback()
            return False

    def get_all_events(self, user): # Méthode pour récupérer tous les événements d'un utilisateur
        self.cursor.execute("SELECT * FROM Event WHERE idUser=? ORDER BY dateTo ASC", (user[0],))
        events = self.cursor.fetchall()
        return events

    def get_next_7_days_events(self, user): # Méthode pour récupérer les événements des 7 prochains jours d'un utilisateur
        end_date = datetime.now() + timedelta(days=7)
        self.cursor.execute("SELECT * FROM Event WHERE idUser=? AND dateTo <= ? ORDER BY dateTo ASC", (user[0], end_date))
        events = self.cursor.fetchall()
        return events
    
    def get_events_between_dates(self, user, date1, date2): # Méthode pour récupérer les événements d'un utilisateur entre deux dates
        # Vérifier si les dates sont au bon format
        valid, message = DatabaseHandler.validate_dates(date1, date2)
        if not valid:
            print(message)
            return
        try:
            self.cursor.execute("SELECT * FROM Event WHERE idUser=? AND dateTo >= ? AND dateFrom <= ? ORDER BY dateTo ASC", (user[0], date1, date2))
            events = self.cursor.fetchall()
            return events
        except ValueError:
            print("Format de date invalide. Utilisez le format YYYY-MM-DD HH:MM.")
    
    def delete_events(self, event_ids): # Méthode pour supprimer des événements, renvoie True si la suppression a réussi, False sinon
        try:
            event_ids = [int(id) for id in event_ids.split(",")]
            placeholders = ",".join("?" * len(event_ids))
            query = "DELETE FROM Event WHERE idEvent IN ({})".format(placeholders)
            self.cursor.execute(query, event_ids)
            self.connection.commit()
            return True
        except Exception as e:
            print("Erreur lors de la suppression des événements:", e)
            self.connection.rollback()
            return False
        

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
            print("Vous ne pouvez pas supprimer votre propre compte.")
            return False
        try:
            self.cursor.execute("SELECT idEvent FROM Event WHERE idUser=?", (idUser,))
            event_ids = [str(row[0]) for row in self.cursor.fetchall()]
            self.delete_events(",".join(event_ids)) # Supprimer les événements associés à l'utilisateur
            self.cursor.execute("DELETE FROM User WHERE idUser=?", (idUser,)) # Supprimer l'utilisateur
            self.connection.commit()
            return True
        except Exception as e:
            print("Erreur lors de la suppression du compte:", e)
            self.connection.rollback()
            return False