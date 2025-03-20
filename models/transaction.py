# models/transaction.py
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