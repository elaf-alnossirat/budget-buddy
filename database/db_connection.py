import mysql.connector
from mysql.connector import pooling, Error

class DBConnection:
    def __init__(self):
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="budget_buddy_pool",
                pool_size=15,  # Augmenté à 15 connexions
                pool_reset_session=True,
                host="localhost",
                user="root",
                password="root",
                database="budget_buddy",
                autocommit=True  # Ajouté pour éviter les verrous
            )
        except Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
            raise  # Propage l'erreur pour un meilleur débogage

    def get_connection(self):
        try:
            return self.pool.get_connection()
        except Error as e:
            print(f"Erreur lors de l'obtention d'une connexion : {e}")
            raise

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        connection = None
        try:
            connection = self.get_connection()
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                
                if fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount
                
                # Pas besoin de commit car autocommit=True
                return result
        except Error as e:
            print(f"Erreur SQL : {e}")
            return None
        finally:
            if connection:
                connection.close()  # Libération explicite