# # models/transaction.py
# class Transaction:
#     def __init__(self, id, user_id, reference, description, amount, date, type, category):
#         self.id = id
#         self.user_id = user_id
#         self.reference = reference
#         self.description = description
#         self.amount = amount
#         self.date = date
#         self.type = type
#         self.category = category


from database.db_connection import DBConnection
from models.user import User  # ✅ Importation correcte


class Transaction:
    def __init__(self, id, user_id, reference, description, amount, date, type, category):
        self.id = id
        self.user_id = user_id
        self.reference = reference
        self.description = description
        self.amount = amount
        self.date = date
        self.type = type
        self.category = category

    @staticmethod
    def create_transaction(user_id, reference, description, amount, date, type, category):
        db = DBConnection()
        
        # 🔥 S'assurer que les retraits et transferts sortants sont négatifs
        if type in ['withdraw', 'transfer_out']:
            amount = -abs(amount)
        elif type in ['deposit', 'transfer_in']:
            amount = abs(amount)

        query = """
        INSERT INTO transactions (user_id, reference, description, amount, date, type, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (user_id, reference, description, amount, date, type, category)
        
        success = db.execute_query(query, params)

        # 🔄 Mettre à jour le solde de l'utilisateur après l'insertion de la transaction
        if success:
            User.update_user_balance(user_id)

        return success
    

    
    @staticmethod
    def get_transactions_by_user(user_id):
        db = DBConnection()
        query = "SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC"
        return db.execute_query(query, (user_id,), fetchall=True)

    @staticmethod
    def get_user_balance(user_id):
        db = DBConnection()
        query = "SELECT get_user_balance(%s) AS balance"
        result = db.execute_query(query, (user_id,), fetchone=True)
        return result["balance"] if result else 0.00




    @staticmethod
    def search_transactions(user_id, **filters):
        """Recherche des transactions avec des filtres optionnels"""
        db = DBConnection()
        base_query = "SELECT * FROM transactions WHERE user_id = %s"
        params = [user_id]
        
        # Construction dynamique de la requête
        if filters:
            conditions = []
            for key, value in filters.items():
                if key == 'start_date' and 'end_date' in filters:
                    conditions.append("date BETWEEN %s AND %s")
                    params.extend([filters['start_date'], filters['end_date']])
                elif key in ['date', 'category', 'type']:
                    conditions.append(f"{key} = %s")
                    params.append(value)
            
            if conditions:
                base_query += " AND " + " AND ".join(conditions)
        
        # Tri
        if 'sort' in filters:
            order = "ASC" if filters['sort'] == "asc" else "DESC"
            base_query += f" ORDER BY amount {order}"
        else:
            base_query += " ORDER BY date DESC"
        
        return db.execute_query(base_query, tuple(params), fetchall=True)