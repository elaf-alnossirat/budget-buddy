# services/transaction_service.py
from database.db_connection import DBConnection
from models.transaction import Transaction

class TransactionService:
    def __init__(self):
        self.db = DBConnection()

    def add_transaction(self, user_id, reference, description, amount, date, type, category):
        """Ajoute une nouvelle transaction."""
        connection = self.db.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO transactions (user_id, reference, description, amount, date, type, category) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (user_id, reference, description, amount, date, type, category))
        connection.commit()
        cursor.close()

    def get_transactions(self, user_id):
        """Récupère toutes les transactions d'un utilisateur."""
        connection = self.db.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
        transactions = cursor.fetchall()
        cursor.close()
        return [Transaction(*transaction) for transaction in transactions]

    def deposit(self, user_id, amount, description="Dépôt"):
        """Dépose de l'argent sur le compte de l'utilisateur."""
        self.add_transaction(user_id, "DEPOSIT", description, amount, "2023-10-01", "deposit", "income")

    def withdraw(self, user_id, amount, description="Retrait"):
        """Retire de l'argent du compte de l'utilisateur."""
        self.add_transaction(user_id, "WITHDRAW", description, -amount, "2023-10-01", "withdrawal", "expense")

    def transfer(self, sender_id, receiver_id, amount, description="Transfert"):
        """Transfère de l'argent vers un autre compte."""
        # Retirer de l'argent du compte de l'expéditeur
        self.add_transaction(sender_id, "TRANSFER_OUT", description, -amount, "2023-10-01", "transfer", "expense")
        # Ajouter de l'argent au compte du destinataire
        self.add_transaction(receiver_id, "TRANSFER_IN", description, amount, "2023-10-01", "transfer", "income")