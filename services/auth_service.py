# services/auth_service.py
from database.db_connection import DBConnection
from models.user import User
import hashlib
import re
from tkinter import messagebox

class AuthService:
    def __init__(self):
        self.db = DBConnection()

    def register_user(self, first_name, last_name, email, password):
        if not self._validate_name(first_name) or not self._validate_name(last_name):
            messagebox.showerror("Invalid Name", "First and last names must be at least 2 characters long.")
            return False
        
        if not self._validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return False
        
        if not self._validate_password(password):
            messagebox.showerror("Invalid Password", "Password must contain at least 10 characters, including uppercase, lowercase, a digit, and a special character.")
            return False
        
        password_hash = self._hash_password(password)
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s)",
                           (first_name, last_name, email, password_hash))
            connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
            return False

    def login_user(self, email, password):
        password_hash = self._hash_password(password)
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s", (email, password_hash))
            user_data = cursor.fetchone()
            cursor.close()
            if user_data:
                return User(*user_data)
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
            return None

    def _validate_name(self, name):
        return len(name) >= 2

    def _validate_email(self, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    def _validate_password(self, password):
        if len(password) < 10:
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        if not re.search("[!@#$%^&*()]", password):
            return False
        return True

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()