# ui/login_ui.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from services.auth_service import AuthService

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Buddy - Connexion")
        self.root.geometry("400x400")
        self.auth_service = AuthService()

        self.main_frame = tb.Frame(root, padding=30)
        self.main_frame.pack(expand=True)

        # Titre
        tb.Label(
            self.main_frame,
            text="Connexion",
            font=("Segoe UI", 20, "bold"),
            bootstyle="info"
        ).pack(pady=(0, 20))

        # Email
        tb.Label(self.main_frame, text="Email", font=("Segoe UI", 12)).pack(anchor="w")
        self.email_entry = tb.Entry(self.main_frame, font=("Segoe UI", 12))
        self.email_entry.pack(fill=X, pady=(0, 10))

        # Mot de passe
        tb.Label(self.main_frame, text="Mot de passe", font=("Segoe UI", 12)).pack(anchor="w")
        self.password_entry = tb.Entry(self.main_frame, font=("Segoe UI", 12), show="*")
        self.password_entry.pack(fill=X, pady=(0, 20))

        # Boutons
        tb.Button(
            self.main_frame,
            text="Connexion",
            bootstyle="success",
            command=self.login
        ).pack(fill=X, pady=5)

        tb.Button(
            self.main_frame,
            text="Créer un compte",
            bootstyle="secondary-outline",
            command=self.open_registration
        ).pack(fill=X, pady=5)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.auth_service.login_user(email, password)
        if user:
          for widget in self.root.winfo_children():
            widget.destroy()  # Efface le contenu du login UI
          import ui.main_ui
          ui.main_ui.MainUI(self.root, user)  # Recharge MainUI dans la même fenêtre
        else:
          messagebox.showerror("Erreur", "Email ou mot de passe invalide.")

    def open_registration(self):
        reg = tb.Toplevel(self.root)
        reg.title("Créer un compte")
        reg.geometry("400x500")

        frame = tb.Frame(reg, padding=30)
        frame.pack(expand=True)

        tb.Label(frame, text="Inscription", font=("Segoe UI", 18, "bold"), bootstyle="info").pack(pady=(0, 20))

        fields = {
            "Prénom": "first_name",
            "Nom": "last_name",
            "Email": "email",
            "Mot de passe": "password"
        }

        self.entries = {}

        for label_text, field in fields.items():
            tb.Label(frame, text=label_text, font=("Segoe UI", 12)).pack(anchor="w")
            entry = tb.Entry(frame, font=("Segoe UI", 12), show="*" if "mot de passe" in label_text.lower() else "")
            entry.pack(fill=X, pady=(0, 10))
            self.entries[field] = entry

        tb.Button(
            frame,
            text="S'inscrire",
            bootstyle="success",
            command=self._register_user
        ).pack(fill=X, pady=10)

    def _register_user(self):
        first_name = self.entries["first_name"].get()
        last_name = self.entries["last_name"].get()
        email = self.entries["email"].get()
        password = self.entries["password"].get()

        if self.auth_service.register_user(first_name, last_name, email, password):
            messagebox.showinfo("Succès", "Compte créé avec succès. Connectez-vous.")
        else:
            messagebox.showerror("Erreur", "Inscription échouée. Vérifiez les champs ou l'email.")
