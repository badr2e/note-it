import tkinter as tk
from tkinter import ttk

class AddCategoryPage(tk.Frame):
    def __init__(self, parent, db, user):
        tk.Frame.__init__(self, parent)
        self.db = db
        self.user = user
        self.configure(bg="#0053f4")
        self.create_widgets()
    
    
    def create_widgets(self):
        title = tk.Label(self, text="Ajouter une catégorie", font=("Arial", 24, "bold"), bg="#0053f4", fg="white")
        title.pack(pady=(20,0))

        frame_listbox = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_listbox.pack(side="left", expand=True, fill='both', padx=(50,10), pady=(10,40))

        scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL) # Ajout d'une barre de défilement à droite et qui se remplit verticalement
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(frame_listbox, yscrollcommand=scrollbar.set, font=("Arial", 11), bg="white", fg="black") # Création d'une liste pour afficher les évènements, on permet la sélection multiple
        self.listbox.pack(expand=True, fill='both')

        scrollbar.config(command=self.listbox.yview) # Configuration de la barre de défilement pour se synchroniser avec la liste

        self.update_category_list()

        #---------Frame Container Entry---------#

        frame_entry = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        frame_entry.pack(side="right", expand=True, fill='both', padx=(10,50), pady=(10,40))

        label_name = tk.Label(frame_entry, text="Nom de la catégorie", bg="white", font=("Arial", 15))
        label_name.pack(fill='x', pady=(100,0))
        self.category_name_entry = tk.Entry(frame_entry, bg="white", fg="black", font=("Arial", 11), bd=1, relief=tk.SOLID)
        self.category_name_entry.pack(pady=(0,5), padx=50, fill='x')

        label_color = tk.Label(frame_entry, text="Couleur", bg="white", font=("Arial", 15))
        label_color.pack(fill='x', pady=(30,0))
        self.color_combobox = ttk.Combobox(frame_entry, state="readonly")
        self.color_combobox.pack(pady=(0,5), padx=50, fill='x')
        self.update_color_combobox()

        btn_add = tk.Button(frame_entry, text="Ajouter", command=self.add_category, font=("Arial", 14))
        btn_add.pack(pady=(10, 20))


    def update_category_list(self):
        self.listbox.delete(0, tk.END)
        categories = self.db.get_user_categories_and_colors(self.user)
        for category in categories:
            category_id, category_name, category_color = category
            self.listbox.insert(tk.END, category_name)
            self.listbox.itemconfig(tk.END, {'bg': category_color, 'fg': 'white'})

    def update_color_combobox(self):
        colors = self.db.get_colors()
        color_values = [color[1] for color in colors]  # Noms des couleurs
        self.color_combobox['values'] = color_values  # Affichez uniquement les noms des couleurs dans la combobox
        self.color_combobox.set("Sélectionner une couleur")  # Texte par défaut

    def add_category(self):
        name = self.category_name_entry.get()
        color_id = self.color_combobox.current()  # Obtenez l'index sélectionné dans la combobox

        if name and color_id != -1:  # Vérifie si le champ de nom de catégorie n'est pas vide et si une couleur est sélectionnée
            success, message = self.db.add_category(self.user, name, color_id+1)
            if success:
                tk.messagebox.showinfo("Succès", message)
                self.listbox.delete(0, tk.END)  # Efface la liste existante
                self.update_category_list()
                self.category_name_entry.delete(0, tk.END)  # Efface le champ de saisie après l'ajout
                self.color_combobox.set("Sélectionner une couleur")  # Réinitialise la combobox de couleur
            else:
                tk.messagebox.showerror("Erreur", message)
        else:
            tk.messagebox.showerror("Erreur", "Veuillez saisir le nom de la catégorie et sélectionner une couleur.")