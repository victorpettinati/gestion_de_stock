import tkinter as tk
from tkinter import ttk, messagebox
from class2gs import DatabaseManager

# Remplacez ces valeurs par celles de votre base de données
host = "localhost"
user = "root"
password = "Laplateforme.06!"
database = "boutique"

db_manager = DatabaseManager(host, user, password, database)

class BoutiqueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Boutique - Gestion des Stocks")
        self.geometry("1000x600")       

        self.create_widgets()

    def create_widgets(self):
        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20)

        # Treeview pour afficher les produits
        self.product_tree = ttk.Treeview(main_frame, columns=("ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie"))
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Nom", text="Nom")
        self.product_tree.heading("Description", text="Description")
        self.product_tree.heading("Prix", text="Prix")
        self.product_tree.heading("Quantité", text="Quantité")
        self.product_tree.heading("ID Catégorie", text="ID Catégorie")
        self.product_tree.column("ID", width=50)
        self.product_tree.column("Nom", width=150)
        self.product_tree.column("Description", width=250)
        self.product_tree.column("Prix", width=100)
        self.product_tree.column("Quantité", width=100)
        self.product_tree.column("ID Catégorie", width=100)
        self.product_tree["show"] = "headings"
        self.product_tree.pack(side="left", fill="both", expand=True)

        # Barre de défilement pour Treeview
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.product_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.product_tree.configure(yscrollcommand=scrollbar.set)

        # Boutons pour gérer les produits
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        self.add_product_button = ttk.Button(button_frame, text="Ajouter un produit", command=self.add_product)
        self.add_product_button.grid(row=0, column=0, padx=5)

        self.edit_product_button = ttk.Button(button_frame, text="Modifier le produit sélectionné", command=self.edit_product)
        self.edit_product_button.grid(row=0, column=1, padx=5)

        self.delete_product_button = ttk.Button(button_frame, text="Supprimer le produit sélectionné", command=self.delete_product)
        self.delete_product_button.grid(row=0, column=2, padx=5)

        # Rafraîchir les produits au démarrage de l'application
        self.refresh_products()

    def refresh_products(self):
        # Effacer tous les éléments actuels
        for i in self.product_tree.get_children():
            self.product_tree.delete(i)

        # Obtenir la liste des produits et les ajouter à l'arbre
        products = db_manager.read_produit()
        for product in products:
            self.product_tree.insert("", "end", values=product)

    def add_product(self):
        add_product_window = tk.Toplevel(self)
        add_product_window.title("Ajouter un produit")
        add_product_window.geometry("400x300")

        form_frame = ttk.Frame(add_product_window)
        form_frame.pack(pady=20)

        # Formulaire pour ajouter un produit
        ttk.Label(form_frame, text="Nom :").grid(row=0, column=0)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Description :").grid(row=1, column=0)
        description_entry = ttk.Entry(form_frame)
        description_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Prix :").grid(row=2, column=0)
        price_entry = ttk.Entry(form_frame)
        price_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Quantité :").grid(row=3, column=0)
        quantity_entry = ttk.Entry(form_frame)
        quantity_entry.grid(row=3, column=1)

        ttk.Label(form_frame, text="ID Catégorie :").grid(row=4, column=0)
        category_id_entry = ttk.Entry(form_frame)
        category_id_entry.grid(row=4, column=1)

        def save_product():
            db_manager.create_produit(
                name_entry.get(),
                description_entry.get(),
                int(price_entry.get()),
                int(quantity_entry.get()),
                int(category_id_entry.get())
            )
            add_product_window.destroy()
            self.refresh_products()

        save_button = ttk.Button(add_product_window, text="Enregistrer", command=save_product)
        save_button.pack(pady=20)

    def edit_product(self):
        selected_product = self.product_tree.focus()
        product_data = self.product_tree.item(selected_product, 'values')

        if not product_data:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à modifier.")
            return

        edit_product_window = tk.Toplevel(self)
        edit_product_window.title("Modifier un produit")
        edit_product_window.geometry("400x300")

        form_frame = ttk.Frame(edit_product_window)
        form_frame.pack(pady=20)

        # Formulaire pour modifier un produit
        ttk.Label(form_frame, text="Nom :").grid(row=0, column=0)
        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, product_data[1])
        name_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Description :").grid(row=1, column=0)
        description_entry = ttk.Entry(form_frame)
        description_entry.insert(0, product_data[2])
        description_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Prix :").grid(row=2, column=0)
        price_entry = ttk.Entry(form_frame)
        price_entry.insert(0, product_data[3])
        price_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Quantité :").grid(row=3, column=0)
        quantity_entry = ttk.Entry(form_frame)
        quantity_entry.insert(0, product_data[4])
        quantity_entry.grid(row=3, column=1)

        ttk.Label(form_frame, text="ID Catégorie :").grid(row=4, column=0)
        category_id_entry = ttk.Entry(form_frame)
        category_id_entry.insert(0, product_data[5])
        category_id_entry.grid(row=4, column=1)

        def update_product():
            db_manager.update_produit(
                int(product_data[0]),
                name_entry.get(),
                description_entry.get(),
                int(price_entry.get()),
                int(quantity_entry.get()),
                int(category_id_entry.get())
            )
            edit_product_window.destroy()
            self.refresh_products()
        
        update_button = ttk.Button(edit_product_window, text="Mettre à jour", command=update_product)
        update_button.pack(pady=20)

    def delete_product(self):
        selected_product = self.product_tree.focus()
        product_data = self.product_tree.item(selected_product, 'values')

        if not product_data:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer.")
            return

        confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce produit ?")
        if confirmation:
            db_manager.delete_produit(int(product_data[0]))
            self.refresh_products()

if __name__ == "__main__":
    app = BoutiqueApp()
    app.mainloop()

