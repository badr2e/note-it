# Note it – Agenda Personnel

Ce projet est une application d'agenda personnel développée en Python. L'application repose sur une base de données SQLite.

Lors de la première inscription dans l'application, l'utilisateur obtient le rôle exclusif d'administrateur, tandis que les inscriptions ultérieures attribuent le rôle d'utilisateur normal.

En tant qu'utilisateur, il est possible de créer un compte, d'ajouter des catégories, d'ajouter des événements, de les visualiser et de les supprimer. L'administrateur, de son côté, dispose de privilèges supplémentaires : il peut consulter le nombre total de comptes et en supprimer.

## Fonctionnement de l'application 

### v0 - Utilisable à partir d'un terminal

### v1 - Interface graphique en tkinter (le mot de passe oublié, l'ajout de catégorie et la recherche d'évènement n'ont pas encore été implémenté)

### v2 - Interface graphique en tkinter plus poussée (le mot de passe oublié, la recherche d'évènement, la sérialisation des données en csv et l'ajout d'évènement régulier n'ont pas encore été implémenté)

#### Installation et Utilisation

1. **Téléchargement du dossier correspondant à la version souhaitée (par exemple, v0) :**
    ```bash
    git clone https://github.com/badr2e/note-it.git
    ```

2. **Lancement du fichier main.py :**
    - Naviguez vers le dossier téléchargé.
    - Exécutez le fichier `main.py`.

3. **Attention vous devez ouvrir le répertoire de la version souhaitée pour lancer le main.py**

#### Fonctionnalités

##### Inscription et Connexion
- L'inscription se fait avec un mail, un nom d'utilisateur et un mot de passe.
- La première inscription crée un administrateur unique, les autres sont des utilisateurs.
- La connexion requiert le nom d'utilisateur et le mot de passe.
- Il est possible de réinitialiser son mot de passe en fournissant son adresse mail + son nom d'utilisateur.

##### Menu Principal Utilisateur
- Ajouter des catégories, ajouter, supprimer et afficher des événements.

##### Menu Principal Admin
- Supprimer un compte
