import sqlite3



class DataBase:
    def __init__(self, bd_file):
        self.connection = sqlite3.connect(bd_file)
        self.cursor = self.connection
        self.connection.execute('CREATE TABLE IF NOT EXISTS users_product (user_id NOT NULL, id_prod NOT NULL,'
                     'name_prod NOT NULL, start_prise NOT NULL, min_prise, prise, link_photo  STRING  NOT NULL,'
                     'link STRING  NOT NULL, valye INTEGER DEFAULT 1)')
        self.connection.execute('CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id UNIQUE NOT NULL,'
                                'activ INTEGER DEFAULT 1)')
        self.connection.commit()



    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO 'users' (user_id) VALUES (?)", (user_id,))
                self.connection.commit()
            except sqlite3.IntegrityError:
                self.cursor.execute("UPDATE users SET activ = 1 WHERE user_id = ?", (user_id,))
                self.connection.commit()

    def off_user(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET activ = 0 WHERE user_id = ?", (user_id,))
            self.connection.commit()

    def select_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users WHERE activ = 1").fetchall()

    def add_product(self, user_id, product: dict):
        bd_user_prod = [user_id]
        bd_user_prod.extend(product.values())
        bd_user_prod.extend([product['salePriceU'], product['salePriceU']])
        with self.connection:
            self.cursor.execute("INSERT INTO 'users_product' (user_id, id_prod, name_prod, start_prise, link_photo, link, min_prise, prise) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", bd_user_prod)
            self.connection.commit()

    def del_product_bd(self, data_id):
        with self.connection:
            self.cursor.execute("DELETE FROM 'users_product' WHERE user_id = ? AND id_prod = ?", data_id)

    def changes_product_data(self, change_data):
        with self.connection:
            self.cursor.execute("UPDATE users_product SET min_prise = ?, prise = ? WHERE user_id = ? AND id_prod = ?", change_data)
            self.connection.commit()

    def changes_product_valye(self,  user_id, product_id, valye):
        with self.connection:
            self.cursor.execute("UPDATE users_product SET valye = ? WHERE user_id = ? AND id_prod = ?", (valye, user_id, product_id,))
            self.connection.commit()

    def all_product_in_user(self, user_id):
        try:
            with self.connection:

                return self.cursor.execute("SELECT * FROM 'users_product' WHERE user_id = ?", (user_id,)).fetchall()

        except sqlite3.OperationalError:
            return False

    def select_user_prod(self, user_id, product_id):
        with self.connection:
            if (
                    self.cursor.execute("SELECT user_id, id_prod FROM users_product WHERE user_id = ? AND id_prod = ?",
                                        (user_id, product_id,)).fetchone()):
                return True
            else:
                return False
