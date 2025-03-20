# ui/login_ui.py
import tkinter as tk
from tkinter import messagebox
from services.auth_service import AuthService

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Buddy - Login")
        self.auth_service = AuthService()

        self.email_label = tk.Label(root, text="Email")
        self.email_label.pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(root, text="Register", command=self.open_registration)
        self.register_button.pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.auth_service.login_user(email, password)
        if user:
            self.root.destroy()
            import ui.main_ui
            main_root = tk.Tk()
            ui.main_ui.MainUI(main_root, user)
            main_root.mainloop()

    def open_registration(self):
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Register")

        first_name_label = tk.Label(registration_window, text="First Name")
        first_name_label.pack()
        first_name_entry = tk.Entry(registration_window)
        first_name_entry.pack()

        last_name_label = tk.Label(registration_window, text="Last Name")
        last_name_label.pack()
        last_name_entry = tk.Entry(registration_window)
        last_name_entry.pack()

        email_label = tk.Label(registration_window, text="Email")
        email_label.pack()
        email_entry = tk.Entry(registration_window)
        email_entry.pack()

        password_label = tk.Label(registration_window, text="Password")
        password_label.pack()
        password_entry = tk.Entry(registration_window, show="*")
        password_entry.pack()

        register_button = tk.Button(registration_window, text="Register", command=lambda: self.register(
            first_name_entry.get(),
            last_name_entry.get(),
            email_entry.get(),
            password_entry.get()
        ))
        register_button.pack()

    def register(self, first_name, last_name, email, password):
        if self.auth_service.register_user(first_name, last_name, email, password):
            self.root.destroy()
            import ui.login_ui
            login_root = tk.Tk()
            ui.login_ui.LoginUI(login_root)
            login_root.mainloop()