# ui/main_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.transaction_service import TransactionService

class MainUI:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Budget Buddy - Main")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.user = user
        self.transaction_service = TransactionService()

        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Welcome message
        self.welcome_label = ttk.Label(self.main_frame, text=f"Welcome, {user.first_name} {user.last_name}", font=("Helvetica", 18, "bold"))
        self.welcome_label.pack(pady=10)

        # Balance summary
        self.balance_label = ttk.Label(self.main_frame, text="Balance: $0.00", font=("Helvetica", 14))
        self.balance_label.pack(pady=10)

        # Buttons for operations
        self.operations_frame = ttk.Frame(self.main_frame)
        self.operations_frame.pack(fill=tk.X, pady=10)

        self.deposit_button = ttk.Button(self.operations_frame, text="Déposer de l'argent", command=self.open_deposit_window, style="Accent.TButton")
        self.deposit_button.pack(side=tk.LEFT, padx=5)

        self.withdraw_button = ttk.Button(self.operations_frame, text="Retirer de l'argent", command=self.open_withdraw_window, style="Accent.TButton")
        self.withdraw_button.pack(side=tk.LEFT, padx=5)

        self.transfer_button = ttk.Button(self.operations_frame, text="Transférer de l'argent", command=self.open_transfer_window, style="Accent.TButton")
        self.transfer_button.pack(side=tk.LEFT, padx=5)

        # Transaction treeview
        self.transaction_tree = ttk.Treeview(self.main_frame, columns=("ID", "Reference", "Description", "Amount", "Date", "Type", "Category"), show="headings")
        self.transaction_tree.heading("ID", text="ID")
        self.transaction_tree.heading("Reference", text="Reference")
        self.transaction_tree.heading("Description", text="Description")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Type", text="Type")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Load transactions and update balance
        self.load_transactions()

    def load_transactions(self):
        """Charge toutes les transactions de l'utilisateur."""
        for row in self.transaction_tree.get_children():
            self.transaction_tree.delete(row)
        transactions = self.transaction_service.get_transactions(self.user.id)
        for transaction in transactions:
            self.transaction_tree.insert("", "end", values=(
                transaction.id,
                transaction.reference,
                transaction.description,
                f"${transaction.amount:.2f}",
                transaction.date,
                transaction.type,
                transaction.category
            ))
        self.update_balance()

    def update_balance(self):
        """Met à jour le solde de l'utilisateur."""
        transactions = self.transaction_service.get_transactions(self.user.id)
        balance = sum(t.amount if t.type == "deposit" else -t.amount for t in transactions)
        self.balance_label.config(text=f"Balance: ${balance:.2f}")

        # Notifier l'utilisateur si le solde est faible
        if balance < 0:
            messagebox.showwarning("Solde faible", "Votre solde est en dessous de zéro!")

    def open_deposit_window(self):
        """Ouvre une fenêtre pour déposer de l'argent."""
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Déposer de l'argent")
        deposit_window.geometry("300x200")
        deposit_window.configure(bg="#f0f0f0")

        # Montant
        amount_label = ttk.Label(deposit_window, text="Montant:", font=("Helvetica", 12))
        amount_label.pack(pady=10)
        amount_entry = ttk.Entry(deposit_window, font=("Helvetica", 12))
        amount_entry.pack(pady=10)

        # Bouton de dépôt
        deposit_button = ttk.Button(deposit_window, text="Déposer", command=lambda: self.deposit(amount_entry.get()), style="Accent.TButton")
        deposit_button.pack(pady=10)

    def deposit(self, amount):
        """Dépose de l'argent sur le compte de l'utilisateur."""
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être supérieur à zéro.")
                return
            self.transaction_service.deposit(self.user.id, amount)
            self.load_transactions()
            messagebox.showinfo("Succès", "Dépôt effectué avec succès!")
            #fermer la fenetre de dépot
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel) and widget.title() == "Déposer de l'argent":
                 widget.destroy()
                 
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

    def open_withdraw_window(self):
        """Ouvre une fenêtre pour retirer de l'argent."""
        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title("Retirer de l'argent")
        withdraw_window.geometry("300x200")
        withdraw_window.configure(bg="#f0f0f0")

        # Montant
        amount_label = ttk.Label(withdraw_window, text="Montant:", font=("Helvetica", 12))
        amount_label.pack(pady=10)
        amount_entry = ttk.Entry(withdraw_window, font=("Helvetica", 12))
        amount_entry.pack(pady=10)

        # Bouton de retrait
        withdraw_button = ttk.Button(withdraw_window, text="Retirer", command=lambda: self.withdraw(amount_entry.get()), style="Accent.TButton")
        withdraw_button.pack(pady=10)

    def withdraw(self, amount):
        """Retire de l'argent du compte de l'utilisateur."""
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être supérieur à zéro.")
                return
            self.transaction_service.withdraw(self.user.id, amount)
            self.load_transactions()
            messagebox.showinfo("Succès", "Retrait effectué avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

    def open_transfer_window(self):
        """Ouvre une fenêtre pour transférer de l'argent."""
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Transférer de l'argent")
        transfer_window.geometry("300x200")
        transfer_window.configure(bg="#f0f0f0")

        # Destinataire
        receiver_label = ttk.Label(transfer_window, text="ID du destinataire:", font=("Helvetica", 12))
        receiver_label.pack(pady=10)
        receiver_entry = ttk.Entry(transfer_window, font=("Helvetica", 12))
        receiver_entry.pack(pady=10)

        # Montant
        amount_label = ttk.Label(transfer_window, text="Montant:", font=("Helvetica", 12))
        amount_label.pack(pady=10)
        amount_entry = ttk.Entry(transfer_window, font=("Helvetica", 12))
        amount_entry.pack(pady=10)

        # Bouton de transfert
        transfer_button = ttk.Button(transfer_window, text="Transférer", command=lambda: self.transfer(receiver_entry.get(), amount_entry.get()), style="Accent.TButton")
        transfer_button.pack(pady=10)

    def transfer(self, receiver_id, amount):
        """Transfère de l'argent vers un autre compte."""
        try:
            receiver_id = int(receiver_id)
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être supérieur à zéro.")
                return
            self.transaction_service.transfer(self.user.id, receiver_id, amount)
            self.load_transactions()
            messagebox.showinfo("Succès", "Transfert effectué avec succès!")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")