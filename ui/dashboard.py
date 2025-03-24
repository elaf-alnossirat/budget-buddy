import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
import calendar
from collections import defaultdict

class DashboardUI:
    def __init__(self, root, user, transaction_service):
        self.root = root
        self.user = user
        self.transaction_service = transaction_service
        
        # Frame principal
        self.dashboard_frame = tb.Frame(root, padding=20)
        
        # Configuration de l'interface
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface du tableau de bord"""
        # En-tête
        header_frame = tb.Frame(self.dashboard_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        tb.Label(
            header_frame,
            text=f"Tableau de bord - {self.user.first_name}",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)
        
        refresh_btn = tb.Button(
            header_frame,
            text="Actualiser",
            command=self.refresh_dashboard,
            bootstyle="info"
        )
        refresh_btn.pack(side=RIGHT)

        # Contenu principal en 2 colonnes
        content_frame = tb.Frame(self.dashboard_frame)
        content_frame.pack(fill=BOTH, expand=True)
        
        # Colonne gauche - Résumé et alertes
        left_frame = tb.Frame(content_frame, padding=10)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Résumé du solde
        self.setup_balance_summary(left_frame)
        
        # Alertes
        self.setup_alerts(left_frame)
        
        # Colonne droite - Graphiques
        right_frame = tb.Frame(content_frame, padding=10)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Graphiques
        self.setup_charts(right_frame)
        
        # Charger les données
        self.refresh_dashboard()
        
    def setup_balance_summary(self, parent):
        """Configure le résumé du solde"""
        summary_frame = tb.LabelFrame(
            parent,
            text="Résumé financier",
            bootstyle="primary",
            padding=10
        )
        summary_frame.pack(fill=X, pady=(0, 10))
        
        # Solde actuel
        current_balance_frame = tb.Frame(summary_frame)
        current_balance_frame.pack(fill=X, pady=5)
        
        tb.Label(
            current_balance_frame,
            text="Solde actuel:",
            font=("Helvetica", 12)
        ).pack(side=LEFT)
        
        self.current_balance_label = tb.Label(
            current_balance_frame,
            text="$0.00",
            font=("Helvetica", 12, "bold"),
            bootstyle="success"
        )
        self.current_balance_label.pack(side=RIGHT)
        
        # Dépenses du mois
        expenses_frame = tb.Frame(summary_frame)
        expenses_frame.pack(fill=X, pady=5)
        
        tb.Label(
            expenses_frame,
            text="Dépenses ce mois:",
            font=("Helvetica", 12)
        ).pack(side=LEFT)
        
        self.expenses_label = tb.Label(
            expenses_frame,
            text="$0.00",
            font=("Helvetica", 12, "bold"),
            bootstyle="danger"
        )
        self.expenses_label.pack(side=RIGHT)
        
        # Revenus du mois
        income_frame = tb.Frame(summary_frame)
        income_frame.pack(fill=X, pady=5)
        
        tb.Label(
            income_frame,
            text="Revenus ce mois:",
            font=("Helvetica", 12)
        ).pack(side=LEFT)
        
        self.income_label = tb.Label(
            income_frame,
            text="$0.00",
            font=("Helvetica", 12, "bold"),
            bootstyle="success"
        )
        self.income_label.pack(side=RIGHT)
        
        # Solde net du mois
        net_frame = tb.Frame(summary_frame)
        net_frame.pack(fill=X, pady=5)
        
        tb.Label(
            net_frame,
            text="Solde net ce mois:",
            font=("Helvetica", 12)
        ).pack(side=LEFT)
        
        self.net_balance_label = tb.Label(
            net_frame,
            text="$0.00",
            font=("Helvetica", 12, "bold")
        )
        self.net_balance_label.pack(side=RIGHT)
        
        # Résumé par mois (3 derniers mois)
        monthly_summary_frame = tb.LabelFrame(
            parent,
            text="Historique des 3 derniers mois",
            bootstyle="primary",
            padding=10
        )
        monthly_summary_frame.pack(fill=X, pady=(10, 0))
        
        # Table pour afficher les données mensuelles
        self.monthly_tree = tb.Treeview(
            monthly_summary_frame,
            columns=("Mois", "Revenus", "Dépenses", "Net"),
            show="headings",
            height=3
        )
        
        # Configuration des colonnes
        self.monthly_tree.heading("Mois", text="Mois")
        self.monthly_tree.heading("Revenus", text="Revenus")
        self.monthly_tree.heading("Dépenses", text="Dépenses")
        self.monthly_tree.heading("Net", text="Net")
        
        self.monthly_tree.column("Mois", width=100, anchor=CENTER)
        self.monthly_tree.column("Revenus", width=80, anchor=E)
        self.monthly_tree.column("Dépenses", width=80, anchor=E)
        self.monthly_tree.column("Net", width=80, anchor=E)
        
        self.monthly_tree.pack(fill=X)
    
    def setup_alerts(self, parent):
        """Configure la section des alertes"""
        alerts_frame = tb.LabelFrame(
            parent,
            text="Alertes et notifications",
            bootstyle="warning",
            padding=10
        )
        alerts_frame.pack(fill=BOTH, expand=True)
        
        # Utilisez le Listbox standard de tkinter
        from tkinter import Listbox
        self.alerts_listbox = Listbox(
            alerts_frame,
            height=8,
            font=("Helvetica", 10),
            bg='white',
            relief='flat'
        )
        self.alerts_listbox.pack(fill=BOTH, expand=True)
        
    def setup_charts(self, parent):
        """Configure les graphiques"""
        charts_notebook = tb.Notebook(parent)
        charts_notebook.pack(fill=BOTH, expand=True)
        
        # Onglet Dépenses par catégorie
        category_tab = tb.Frame(charts_notebook, padding=10)
        charts_notebook.add(category_tab, text="Dépenses par catégorie")
        
        self.category_chart_frame = tb.Frame(category_tab)
        self.category_chart_frame.pack(fill=BOTH, expand=True)
        
        # Onglet Évolution du solde
        balance_tab = tb.Frame(charts_notebook, padding=10)
        charts_notebook.add(balance_tab, text="Évolution du solde")
        
        self.balance_chart_frame = tb.Frame(balance_tab)
        self.balance_chart_frame.pack(fill=BOTH, expand=True)
        
        # Onglet Revenus vs Dépenses
        comparison_tab = tb.Frame(charts_notebook, padding=10)
        charts_notebook.add(comparison_tab, text="Revenus vs Dépenses")
        
        self.comparison_chart_frame = tb.Frame(comparison_tab)
        self.comparison_chart_frame.pack(fill=BOTH, expand=True)
    
    def refresh_dashboard(self):
        """Actualise toutes les données du tableau de bord"""
        try:
            # Récupérer les transactions
            transactions = self.transaction_service.get_transactions(self.user.id)
            
            # Mettre à jour le résumé du solde
            self.update_balance_summary(transactions)
            
            # Mettre à jour les alertes
            self.update_alerts(transactions)
            
            # Mettre à jour les graphiques
            self.update_charts(transactions)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de rafraîchir le tableau de bord: {str(e)}")
    
    def update_balance_summary(self, transactions):
        """Met à jour le résumé du solde"""
        # Solde actuel
        current_balance = self.transaction_service.get_balance(self.user.id)
        self.current_balance_label.config(
            text=f"${current_balance:,.2f}",
            bootstyle="success" if current_balance >= 0 else "danger"
        )
        
        # Calculer les transactions du mois en cours
        current_month = datetime.now().strftime('%Y-%m')
        monthly_transactions = [t for t in transactions if t.date.startswith(current_month)]
        
        # Calculer les dépenses, revenus et solde net du mois
        expenses = sum(t.amount for t in monthly_transactions if t.amount < 0)
        income = sum(t.amount for t in monthly_transactions if t.amount > 0)
        net_balance = income + expenses  # expenses est déjà négatif
        
        self.expenses_label.config(text=f"${abs(expenses):,.2f}")
        self.income_label.config(text=f"${income:,.2f}")
        self.net_balance_label.config(
            text=f"${net_balance:,.2f}",
            bootstyle="success" if net_balance >= 0 else "danger"
        )
        
        # Mettre à jour le résumé des 3 derniers mois
        self.update_monthly_summary(transactions)
    
    def update_monthly_summary(self, transactions):
        """Met à jour le résumé des 3 derniers mois"""
        # Vider la liste actuelle
        self.monthly_tree.delete(*self.monthly_tree.get_children())
        
        # Calculer les 3 derniers mois
        now = datetime.now()
        months_data = []
        
        for i in range(3):
            month_date = now - timedelta(days=30*i)
            month_str = month_date.strftime('%Y-%m')
            month_name = month_date.strftime('%b %Y')
            
            # Filtrer les transactions du mois
            month_transactions = [t for t in transactions if t.date.startswith(month_str)]
            
            # Calculer revenus et dépenses
            income = sum(t.amount for t in month_transactions if t.amount > 0)
            expenses = sum(t.amount for t in month_transactions if t.amount < 0)
            net = income + expenses  # expenses est déjà négatif
            
            months_data.append((month_name, income, expenses, net))
        
        # Afficher les données
        for month_name, income, expenses, net in months_data:
            self.monthly_tree.insert(
                "",
                "end",
                values=(
                    month_name,
                    f"${income:,.2f}",
                    f"${abs(expenses):,.2f}",
                    f"${net:,.2f}"
                ),
                tags=('positive' if net >= 0 else 'negative',)
            )
        
        # Configurer les couleurs
        self.monthly_tree.tag_configure('positive', foreground='green')
        self.monthly_tree.tag_configure('negative', foreground='red')
    
    def update_alerts(self, transactions):
        """Met à jour les alertes et notifications"""
        # Vider la liste des alertes
        self.alerts_listbox.delete(0, END)
        
        # Vérifier le solde actuel
        current_balance = self.transaction_service.get_balance(self.user.id)
        
        alerts = []
        
        # Alerte de découvert
        if current_balance < 0:
            alerts.append(f"⚠️ ALERTE: Votre compte est à découvert (${current_balance:,.2f})")
        
        # Alerte de solde faible
        elif current_balance < 100:
            alerts.append(f"⚠️ Attention: Votre solde est faible (${current_balance:,.2f})")
        
        # Calculer les dépenses du mois en cours
        now = datetime.now()
        current_month = now.strftime('%Y-%m')
        monthly_transactions = [t for t in transactions if t.date.startswith(current_month)]
        
        expenses = sum(t.amount for t in monthly_transactions if t.amount < 0)
        income = sum(t.amount for t in monthly_transactions if t.amount > 0)
        
        # Alerte si les dépenses sont supérieures aux revenus
        if abs(expenses) > income:
            alerts.append(f"📉 Ce mois-ci, vos dépenses (${abs(expenses):,.2f}) dépassent vos revenus (${income:,.2f})")
        
        # Vérifier les grosses dépenses récentes (30 derniers jours)
        recent_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')
        recent_transactions = [t for t in transactions if t.date >= recent_date and t.amount < -100]
        
        if recent_transactions:
            alerts.append(f"💸 {len(recent_transactions)} dépenses importantes (> $100) au cours des 30 derniers jours")
            for t in recent_transactions[:3]:  # Limiter à 3 pour éviter de surcharger
                alerts.append(f"  • {t.date}: {t.description} (${abs(t.amount):,.2f})")
        
        # Ajouter à la listbox
        if alerts:
            for alert in alerts:
                self.alerts_listbox.insert(END, alert)
        else:
            self.alerts_listbox.insert(END, "✅ Aucune alerte - Tout est en ordre!")
    
    def update_charts(self, transactions):
        """Met à jour tous les graphiques"""
        self.update_category_chart(transactions)
        self.update_balance_chart(transactions)
        self.update_comparison_chart(transactions)
    
    def update_category_chart(self, transactions):
        """Met à jour le graphique des dépenses par catégorie"""
        # Supprimer le graphique existant s'il y en a un
        for widget in self.category_chart_frame.winfo_children():
            widget.destroy()
        
        # Filtrer les dépenses des 30 derniers jours
        recent_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        expenses = [t for t in transactions if t.date >= recent_date and t.amount < 0]
        
        # Regrouper par catégorie
        categories = defaultdict(float)
        for t in expenses:
            categories[t.category] += abs(t.amount)
        
        if not categories:
            # S'il n'y a pas de dépenses, afficher un message
            tb.Label(
                self.category_chart_frame,
                text="Aucune dépense dans les 30 derniers jours",
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(expand=True)
            return
        
        # Créer le graphique camembert
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        wedges, texts, autotexts = ax.pie(
            categories.values(),
            labels=categories.keys(),
            autopct=lambda p: f'{p:.1f}%\n(${p*sum(categories.values())/100:,.2f})',
            startangle=90,
            shadow=True,
            textprops={'fontsize': 8}
        )
        ax.axis('equal')  # Pour que le camembert soit circulaire
        plt.title('Dépenses par catégorie (30 derniers jours)')
        
        # Intégrer le graphique dans l'interface
        canvas = FigureCanvasTkAgg(fig, master=self.category_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    def update_balance_chart(self, transactions):
        """Met à jour le graphique d'évolution du solde"""
        # Supprimer le graphique existant s'il y en a un
        for widget in self.balance_chart_frame.winfo_children():
            widget.destroy()
        
        if not transactions:
            # S'il n'y a pas de transactions, afficher un message
            tb.Label(
                self.balance_chart_frame,
                text="Aucune transaction à afficher",
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(expand=True)
            return
        
        # Trier les transactions par date
        sorted_transactions = sorted(transactions, key=lambda t: t.date)
        
        # Créer des points de données pour l'évolution du solde
        dates = []
        balances = []
        running_balance = 0
        
        for t in sorted_transactions:
            dates.append(t.date)
            running_balance += t.amount
            balances.append(running_balance)
        
        # Créer le graphique linéaire
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.plot(dates, balances, marker='o', linestyle='-', color='blue')
        
        # Ajouter une ligne horizontale à zéro
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.3)
        
        # Formater l'axe des x pour qu'il soit lisible
        ax.set_xticks(dates[::max(1, len(dates)//5)])  # Afficher ~5 dates
        ax.tick_params(axis='x', rotation=45)
        
        plt.title('Évolution du solde')
        plt.tight_layout()
        
        # Intégrer le graphique dans l'interface
        canvas = FigureCanvasTkAgg(fig, master=self.balance_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    def update_comparison_chart(self, transactions):
        """Met à jour le graphique de comparaison revenus/dépenses"""
        # Supprimer le graphique existant s'il y en a un
        for widget in self.comparison_chart_frame.winfo_children():
            widget.destroy()
        
        if not transactions:
            # S'il n'y a pas de transactions, afficher un message
            tb.Label(
                self.comparison_chart_frame,
                text="Aucune transaction à afficher",
                font=("Helvetica", 12),
                bootstyle="secondary"
            ).pack(expand=True)
            return
        
        # Regrouper les transactions par mois
        monthly_data = defaultdict(lambda: {"income": 0, "expenses": 0})
        
        for t in transactions:
            month = t.date[:7]  # Format YYYY-MM
            if t.amount > 0:
                monthly_data[month]["income"] += t.amount
            else:
                monthly_data[month]["expenses"] += abs(t.amount)
        
        # Trier les mois
        months = sorted(monthly_data.keys())
        
        # Extraire les données pour le graphique
        incomes = [monthly_data[m]["income"] for m in months]
        expenses = [monthly_data[m]["expenses"] for m in months]
        
        # Convertir les YYYY-MM en noms de mois plus lisibles
        month_labels = []
        for m in months:
            year, month = m.split('-')
            month_name = calendar.month_abbr[int(month)]
            month_labels.append(f"{month_name} {year}")
        
        # Créer le graphique à barres
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        
        x = range(len(months))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], incomes, width, label='Revenus', color='green', alpha=0.7)
        ax.bar([i + width/2 for i in x], expenses, width, label='Dépenses', color='red', alpha=0.7)
        
        ax.set_xticks(x)
        ax.set_xticklabels(month_labels, rotation=45)
        ax.legend()
        
        plt.title('Revenus vs Dépenses par mois')
        plt.tight_layout()
        
        # Intégrer le graphique dans l'interface
        canvas = FigureCanvasTkAgg(fig, master=self.comparison_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    def show(self):
        """Affiche le tableau de bord"""
        self.dashboard_frame.pack(fill=BOTH, expand=True)
    
    def hide(self):
        """Cache le tableau de bord"""
        self.dashboard_frame.pack_forget()