# database/db_connection.py
import mysql.connector

class DBConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="budget_buddy"
        )
    
    def get_connection(self):
        return self.connection
    
    def close_connection(self):
        self.connection.close()