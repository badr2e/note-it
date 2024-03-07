# Note it – Agenda Personnel

# v0

Ce projet est une application d'agenda personnel en python, utilisable à partir d'un terminal.

## Installation et Utilisation

Pour utiliser cette version du projet, suivez ces étapes :
1. Assurez-vous d'avoir les modules suivants installés :
    - sqlite3
    - os
    - hashlib
    - re
    - datetime

    ```bash
    pip install sqlite3 os hashlib re datetime
    ```

2. Clonez le dossier `v0` :
    ```bash
    git clone https://https://github.com/badr2e/noteit/tree/v0
    ```

3. Lancez le fichier `main.py`.

## Fonctionnalités

### Étape 1 : Inscription et Connexion
- L'inscription se fait avec un mail, un nom d'utilisateur et un mot de passe.
- La première inscription crée un administrateur unique, les autres sont des utilisateurs.
- La connexion requiert le nom d'utilisateur et le mot de passe.
- Il est possible de réinitialiser son mot de passe en fournissant son adresse mail + son nom d'utilisateur.

### Étape 2 : Menu Principal Utilisateur
- Ajouter, supprimer et afficher les événements.
#### Fonctionnalités détaillées :
- **Ajouter un événement :**
  - Nommer l'évènement.
  - Ajouter une description (optionnel).
  - Écrire la date de début de l'évènement.
  - Écrire la date de fin de l'évènement.
- **Supprimer un événement :**
  - Affichage de toutes les tâches avec un identifiant à côté.
  - Entrer les identifiants des événements à supprimer séparés par une virgule.
- **Afficher les événements (sous-menu) :**
  - Afficher tous les événements (sans les événements passés).
  - Afficher les tâches des 7 prochains jours.
  - Afficher les tâches sur des laps de temps précis.
- Options pour retourner au menu ou se déconnecter.

### Étape 2bis : Menu Principal Admin
- Afficher le nombre de comptes dans l'application et supprimer un compte.
#### Fonctionnalités détaillées :
- **Afficher le nombre de comptes.**
- **Supprimer un compte :**
  - Affichage de tous les comptes de l'application avec l'ID, l'email et le nom d'utilisateur.
  - L'admin entre l'ID du compte à supprimer.

### Étape 3 : Déconnexion
- Retour à l'étape 1 pour se connecter ou créer un nouveau compte.