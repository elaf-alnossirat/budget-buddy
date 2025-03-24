import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from services.transaction_service import TransactionService

class MainUI:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Budget Buddy - Tableau de bord")
        self.root.geometry("900x650")
        self.user = user
        self.transaction_service = TransactionService()

        # Frame principale avec style
        self.main_frame = tb.Frame(root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)

        # 🎨 Menu de sélection de thème
        self.theme_menu = tb.Menubutton(
            self.main_frame,
            text="🎨 Thème",
            bootstyle="secondary"
        )

        def change_theme(self, theme_name):
            print(f"Thème sélectionné : {theme_name}")  # pour debug
        self.root.style.theme_use(theme_name)
        self.theme_menu.pack(anchor="ne", padx=10, pady=10)

        menu = tb.Menu(self.theme_menu)
        self.theme_menu["menu"] = menu

        themes = [("Clair", "flatly"), ("Sombre", "superhero")]

        for label, theme_name in themes:
            menu.add_command(label=label, command=lambda t=theme_name: self.change_theme(t))

        # Message de bienvenue
        self.welcome_label = tb.Label(
            self.main_frame,
            text=f"Bienvenue, {user.first_name} {user.last_name}",
            font=("Segoe UI", 20, "bold"),
            bootstyle="info"
        )
        self.welcome_label.pack(pady=(0, 10), anchor="w")

        # Solde
        self.balance_label = tb.Label(
            self.main_frame,
            text="Solde: $0.00",
            font=("Segoe UI", 16, "bold"),
            bootstyle="success"
        )
        self.balance_label.pack(pady=(0, 20), anchor="w")

        # Boutons d'opérations
        self.operations_frame = tb.Frame(self.main_frame)
        self.operations_frame.pack(fill=X, pady=10)

        self.deposit_button = tb.Button(
            self.operations_frame,
            text="Déposer",
            command=self.open_deposit_window,
            bootstyle="success-outline"
        )
        self.deposit_button.pack(side=LEFT, padx=5)

        self.withdraw_button = tb.Button(
            self.operations_frame,
            text="Retirer",
            command=self.open_withdraw_window,
            bootstyle="danger-outline"
        )
        self.withdraw_button.pack(side=LEFT, padx=5)

        self.transfer_button = tb.Button(
            self.operations_frame,
            text="Transférer",
            command=self.open_transfer_window,
            bootstyle="warning-outline"
        )
        self.transfer_button.pack(side=LEFT, padx=5)

        # Liste des transactions
        self.transaction_tree = tb.Treeview(
            self.main_frame,
            columns=("ID", "Réf", "Description", "Montant", "Date", "Type", "Catégorie"),
            show="headings",
            height=15,
            bootstyle="dark"
        )

        for col in self.transaction_tree["columns"]:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, anchor="center", width=110)

        self.transaction_tree.pack(fill=BOTH, expand=True, pady=20)

        # Chargement initial
        self.load_transactions()

    # 🔄 Méthode pour changer de thème
    def change_theme(self, theme_name):
        self.root.style.theme_use(theme_name)

    def load_transactions(self):
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        transactions = self.transaction_service.get_transactions(self.user.id)
        for t in transactions:
            self.transaction_tree.insert("", "end", values=(
                t.id,
                t.reference,
                t.description,
                f"${t.amount:.2f}",
                t.date,
                t.type,
                t.category
            ))
        self.update_balance()

    def update_balance(self):
        transactions = self.transaction_service.get_transactions(self.user.id)
        balance = sum(t.amount if t.type == "deposit" else -t.amount for t in transactions)
        self.balance_label.config(text=f"Solde: ${balance:.2f}")
        if balance < 0:
            messagebox.showwarning("Solde faible", "Votre solde est en dessous de zéro!")

    def open_deposit_window(self):
        self._open_amount_window("Déposer", self.deposit, "success")

    def open_withdraw_window(self):
        self._open_amount_window("Retirer", self.withdraw, "danger")

    def open_transfer_window(self):
        transfer_window = tb.Toplevel(self.root)
        transfer_window.title("Transférer de l'argent")
        transfer_window.geometry("350x250")
        transfer_window.resizable(False, False)
        transfer_window.configure(padx=20, pady=20)

        tb.Label(transfer_window, text="ID du destinataire:", font=("Segoe UI", 12)).pack(pady=(0, 10))
        receiver_entry = tb.Entry(transfer_window, font=("Segoe UI", 12))
        receiver_entry.pack(fill=X, pady=(0, 20))

        tb.Label(transfer_window, text="Montant:", font=("Segoe UI", 12)).pack()
        amount_entry = tb.Entry(transfer_window, font=("Segoe UI", 12))
        amount_entry.pack(fill=X, pady=(0, 20))

        tb.Button(
            transfer_window,
            text="Transférer",
            bootstyle="warning",
            command=lambda: self.transfer(receiver_entry.get(), amount_entry.get(), transfer_window)
        ).pack()

    def _open_amount_window(self, title, callback, style):
        window = tb.Toplevel(self.root)
        window.title(title)
        window.geometry("300x200")
        window.resizable(False, False)
        window.configure(padx=20, pady=20)

        tb.Label(window, text="Montant:", font=("Segoe UI", 12)).pack(pady=(0, 10))
        amount_entry = tb.Entry(window, font=("Segoe UI", 12))
        amount_entry.pack(fill=X, pady=(0, 20))

        tb.Button(
            window,
            text=title,
            bootstyle=style,
            command=lambda: callback(amount_entry.get(), window)
        ).pack()

    def deposit(self, amount, window):
        try:
            amount = float(amount)
            if amount <= 0:
                return messagebox.showerror("Erreur", "Le montant doit être positif.")
            self.transaction_service.deposit(self.user.id, amount)
            self.load_transactions()
            window.destroy()
            messagebox.showinfo("Succès", "Dépôt effectué avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide.")

    def withdraw(self, amount, window):
        try:
            amount = float(amount)
            if amount <= 0:
                return messagebox.showerror("Erreur", "Le montant doit être positif.")
            self.transaction_service.withdraw(self.user.id, amount)
            self.load_transactions()
            window.destroy()
            messagebox.showinfo("Succès", "Retrait effectué avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide.")

    def transfer(self, receiver_id, amount, window):
        try:
            receiver_id = int(receiver_id)
            amount = float(amount)
            if amount <= 0:
                return messagebox.showerror("Erreur", "Le montant doit être positif.")
            self.transaction_service.transfer(self.user.id, receiver_id, amount)
            self.load_transactions()
            window.destroy()
            messagebox.showinfo("Succès", "Transfert effectué avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Entrées invalides.")
