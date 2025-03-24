import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from services.transaction_service import TransactionService
from ui.dashboard import DashboardUI

class MainUI:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Budget Buddy")
        self.root.geometry("1000x700")
        self.user = user
        self.transaction_service = TransactionService()
        self.dashboard_ui = None  # Référence au tableau de bord

        # Configuration de l'interface
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        self.main_frame = tb.Frame(self.root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)

        # En-tête
        self.setup_header()

        # Filtres
        self.setup_filters()

        # Liste des transactions
        self.setup_transaction_list()

        self.load_transactions()

    def setup_header(self):
        """Configure l'en-tête"""
        # Message de bienvenue
        tb.Label(
            self.main_frame,
            text=f"Bienvenue, {self.user.first_name}",
            font=("Helvetica", 16),
            bootstyle="primary"
        ).pack(anchor="nw", pady=10)

        # Solde
        self.balance_label = tb.Label(
            self.main_frame,
            text="Solde: $0.00",
            font=("Helvetica", 14),
            bootstyle="success"
        )
        self.balance_label.pack(anchor="nw", pady=5)

        # Boutons d'opérations
        btn_frame = tb.Frame(self.main_frame)
        btn_frame.pack(fill=X, pady=10)

        tb.Button(
            btn_frame,
            text="Déposer",
            command=self.open_deposit_window,
            bootstyle="success"
        ).pack(side=LEFT, padx=5)

        tb.Button(
            btn_frame,
            text="Retirer",
            command=self.open_withdraw_window,
            bootstyle="danger"
        ).pack(side=LEFT, padx=5)

        tb.Button(
            btn_frame,
            text="Transférer",
            command=self.open_transfer_window,
            bootstyle="warning"
        ).pack(side=LEFT, padx=5)

        # Nouveau bouton pour le tableau de bord
        tb.Button(
            btn_frame,
            text="Tableau de bord",
            command=self.show_dashboard,
            bootstyle="info"
        ).pack(side=RIGHT, padx=5)

    def show_dashboard(self):
        """Affiche le tableau de bord"""
        if self.dashboard_ui is None:
            self.dashboard_ui = DashboardUI(self.root, self.user, self.transaction_service)
        
        # Cacher l'interface principale
        self.main_frame.pack_forget()
        
        # Afficher le tableau de bord
        self.dashboard_ui.show()

    def setup_filters(self):
        """Configure les filtres"""
        filter_frame = tb.Frame(self.main_frame)
        filter_frame.pack(fill=X, pady=10)

        # Filtre Date
        tb.Label(filter_frame, text="Date:").pack(side=LEFT, padx=5)
        self.date_entry = tb.DateEntry(filter_frame)
        self.date_entry.pack(side=LEFT, padx=5)

        # Filtre Catégorie
        tb.Label(filter_frame, text="Catégorie:").pack(side=LEFT, padx=5)
        self.category_combo = tb.Combobox(
            filter_frame,
            values=["", "leisure", "meal", "bribe", "income", "expense"],
            width=12
        )
        self.category_combo.pack(side=LEFT, padx=5)

        # Filtre Type
        tb.Label(filter_frame, text="Type:").pack(side=LEFT, padx=5)
        self.type_combo = tb.Combobox(
            filter_frame,
            values=["", "deposit", "withdrawal", "transfer"],
            width=12
        )
        self.type_combo.pack(side=LEFT, padx=5)

        # Bouton Appliquer
        tb.Button(
            filter_frame,
            text="Appliquer filtres",
            command=self.apply_filters,
            bootstyle="primary"
        ).pack(side=LEFT, padx=10)

        # Bouton Réinitialiser
        tb.Button(
            filter_frame,
            text="Réinitialiser",
            command=self.reset_filters,
            bootstyle="secondary"
        ).pack(side=LEFT)

    def setup_transaction_list(self):
        """Configure la liste des transactions"""
        self.transaction_tree = tb.Treeview(
            self.main_frame,
            columns=("ID", "Réf", "Description", "Montant", "Date", "Type", "Catégorie"),
            show="headings",
            height=15
        )

        # Configuration des colonnes
        columns = [
            ("ID", 50, "center"),
            ("Réf", 80, "center"),
            ("Description", 200, "w"),
            ("Montant", 100, "e"),
            ("Date", 100, "center"),
            ("Type", 100, "center"),
            ("Catégorie", 120, "center")
        ]

        for col, width, anchor in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=width, anchor=anchor)

        scrollbar = tb.Scrollbar(self.main_frame, orient=VERTICAL, command=self.transaction_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        self.transaction_tree.pack(fill=BOTH, expand=True)

    def apply_filters(self):
        """Applique les filtres sélectionnés"""
        criteria = {}
        
        if self.date_entry.entry.get():
            criteria['date'] = self.date_entry.entry.get()
        
        if self.category_combo.get():
            criteria['category'] = self.category_combo.get()
        
        if self.type_combo.get():
            criteria['type'] = self.type_combo.get()
        
        transactions = self.transaction_service.search_transactions(self.user.id, criteria)
        self.update_transaction_list(transactions)

    def reset_filters(self):
        """Réinitialise les filtres"""
        self.date_entry.entry.delete(0, END)
        self.category_combo.set('')
        self.type_combo.set('')
        self.load_transactions()

    def load_transactions(self):
        """Charge toutes les transactions"""
        transactions = self.transaction_service.get_transactions(self.user.id)
        self.update_transaction_list(transactions)

    def update_transaction_list(self, transactions):
        """Met à jour l'affichage des transactions"""
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        
        for t in transactions:
            self.transaction_tree.insert("", END, values=(
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
        """Met à jour l'affichage du solde"""
        balance = self.transaction_service.get_balance(self.user.id)
        self.balance_label.config(text=f"Solde: ${balance:.2f}")

    # ... (méthodes open_deposit_window, open_withdraw_window, etc. restent inchangées)

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