# # models/user.py
# class User:
#     def __init__(self, id, first_name, last_name, email, password_hash):
#         self.id = id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.password_hash = password_hash


from database.db_connection import DBConnection

class User:
    def __init__(self, id, first_name, last_name, email, password_hash, balance=0.00):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.balance = balance

    @staticmethod
    def create_user(first_name, last_name, email, password_hash):
        db = DBConnection()
        query = """
        INSERT INTO users (first_name, last_name, email, password_hash, balance)
        VALUES (%s, %s, %s, %s, 0.00)
        """
        params = (first_name, last_name, email, password_hash)
        return db.execute_query(query, params)

    @staticmethod
    def get_user_by_email(email):
        db = DBConnection()
        query = "SELECT * FROM users WHERE email = %s"
        return db.execute_query(query, (email,), fetchone=True)

    @staticmethod
    def user_exists(email):
        return User.get_user_by_email(email) is not None

    @staticmethod
    def update_user_balance(user_id):
        db = DBConnection()
        query = """
        UPDATE users 
        SET balance = (SELECT get_user_balance(%s))
        WHERE id = %s
        """
        params = (user_id, user_id)
        return db.execute_query(query, params)
