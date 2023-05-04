import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    # CRUD operations for 'produit' table
    def create_produit(self, nom, description, prix, quantite, id_categorie):
        query = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
        values = (nom, description, prix, quantite, id_categorie)
        self.cursor.execute(query, values)
        self.conn.commit()

    def read_produit(self, produit_id=None):
        query = "SELECT * FROM produit"
        if produit_id:
            query += " WHERE id = %s"
            self.cursor.execute(query, (produit_id,))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_produit(self, produit_id, nom=None, description=None, prix=None, quantite=None, id_categorie=None):
        query = "UPDATE produit SET "
        params = []
        values = []

        if nom:
            params.append("nom = %s")
            values.append(nom)
        if description:
            params.append("description = %s")
            values.append(description)
        if prix:
            params.append("prix = %s")
            values.append(prix)
        if quantite:
            params.append("quantite = %s")
            values.append(quantite)
        if id_categorie:
            params.append("id_categorie = %s")
            values.append(id_categorie)

        query += ", ".join(params) + " WHERE id = %s"
        values.append(produit_id)

        self.cursor.execute(query, values)
        self.conn.commit()


    def delete_produit(self, produit_id):
        query = "DELETE FROM produit WHERE id = %s"
        self.cursor.execute(query, (produit_id,))
        self.conn.commit()

    # CRUD operations for 'categorie' table
    def create_categorie(self, nom):
        query = "INSERT INTO categorie (nom) VALUES (%s)"
        self.cursor.execute(query, (nom,))
        self.conn.commit()

    def read_categorie(self, categorie_id=None):
        query = "SELECT * FROM categorie"
        if categorie_id:
            query += " WHERE id = %s"
            self.cursor.execute(query, (categorie_id,))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_categorie(self, categorie_id, nom):
        query = "UPDATE categorie SET nom = %s WHERE id = %s"
        self.cursor.execute(query, (nom, categorie_id))
        self.conn.commit()

    def delete_categorie(self, categorie_id):
        query = "DELETE FROM categorie WHERE id = %s"
        self.cursor.execute(query, (categorie_id,))
        self.conn.commit()
