from database.db_connection import DBConnection
from models.transaction import Transaction
from datetime import datetime

class TransactionService:
    def __init__(self):
        self.db = DBConnection()

    def add_transaction(self, user_id, reference, description, amount, date, type, category):
        """Ajoute une nouvelle transaction"""
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        if type in ['withdrawal', 'transfer']:
            amount = -abs(amount)
        
        cursor.execute(
            """INSERT INTO transactions (user_id, reference, description, amount, date, type, category) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (user_id, reference, description, amount, date, type, category)
        )
        connection.commit()
        cursor.close()
        self.update_balance(user_id)

    def get_transactions(self, user_id):
        """Récupère toutes les transactions"""
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC", (user_id,))
        transactions = cursor.fetchall()
        cursor.close()
        return [Transaction(**t) for t in transactions]

    def get_balance(self, user_id):
        """Calcule le solde"""
        connection = self.db.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        balance = float(result[0]) if result[0] is not None else 0.0
        cursor.close()
        return balance

    def update_balance(self, user_id):
        """Met à jour le solde"""
        connection = self.db.get_connection()
        cursor = connection.cursor()
        new_balance = self.get_balance(user_id)
        
        cursor.execute("""
            INSERT INTO user_balances (user_id, balance)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE balance = VALUES(balance)
            """, 
            (user_id, new_balance)
        )
        connection.commit()
        cursor.close()

    def deposit(self, user_id, amount, description="Dépôt"):
        """Effectue un dépôt"""
        self.add_transaction(
            user_id, "DEPOSIT", description, 
            abs(amount), datetime.now().strftime('%Y-%m-%d'), 
            "deposit", "income"
        )

    def withdraw(self, user_id, amount, description="Retrait"):
        """Effectue un retrait"""
        self.add_transaction(
            user_id, "WITHDRAW", description,
            abs(amount), datetime.now().strftime('%Y-%m-%d'),
            "withdrawal", "expense"
        )

    def transfer(self, sender_id, receiver_id, amount, description="Transfert"):
        """Effectue un transfert"""
        self.add_transaction(
            sender_id, "TRANSFER_OUT", description,
            abs(amount), datetime.now().strftime('%Y-%m-%d'),
            "transfer", "expense"
        )
        self.add_transaction(
            receiver_id, "TRANSFER_IN", description,
            abs(amount), datetime.now().strftime('%Y-%m-%d'),
            "transfer", "income"
        )

    def search_transactions(self, user_id, criteria):
        """Filtre les transactions selon les critères"""
        base_query = "SELECT * FROM transactions WHERE user_id = %s"
        params = [user_id]
        conditions = []
        
        if criteria.get('date'):
            conditions.append("date = %s")
            params.append(criteria['date'])
        
        if criteria.get('category'):
            conditions.append("category = %s")
            params.append(criteria['category'])
        
        if criteria.get('type'):
            conditions.append("type = %s")
            params.append(criteria['type'])
        
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
        
        base_query += " ORDER BY date DESC"
        
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(base_query, tuple(params))
        transactions = cursor.fetchall()
        cursor.close()
        
        return [Transaction(**t) for t in transactions]
        
    def get_monthly_summary(self, user_id, start_date=None, end_date=None):
        """Récupère un résumé mensuel des transactions"""
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            DATE_FORMAT(date, '%Y-%m') as month,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as expenses
        FROM transactions 
        WHERE user_id = %s
        """
        params = [user_id]
        
        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)
        
        query += " GROUP BY DATE_FORMAT(date, '%Y-%m') ORDER BY month DESC"
        
        cursor.execute(query, tuple(params))
        summary = cursor.fetchall()
        cursor.close()
        
        return summary
    
    def get_category_summary(self, user_id, start_date=None, end_date=None):
        """Récupère un résumé des dépenses par catégorie"""
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            category,
            SUM(ABS(amount)) as total
        FROM transactions 
        WHERE user_id = %s AND amount < 0
        """
        params = [user_id]
        
        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)
        
        query += " GROUP BY category ORDER BY total DESC"
        
        cursor.execute(query, tuple(params))
        summary = cursor.fetchall()
        cursor.close()
        
        return summary
    
    def check_balance_threshold(self, user_id, threshold=0):
        """Vérifie si le solde est inférieur à un seuil donné"""
        balance = self.get_balance(user_id)
        return balance < threshold