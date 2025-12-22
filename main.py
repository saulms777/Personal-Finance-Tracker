#!/usr/bin/env python3
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from finance_tracker import PersonalFinanceTracker
from visualizer import FinanceVisualizer
from demo import run_full_demo, create_sample_data

from datetime import datetime
current_date = datetime.now()

def main():
    """Main function to run the finance tracker"""
    print("💰 Personal Finance Tracker")
    print("=" * 40)
    print("1. Run Full Demonstration")
    print("2. Interactive Mode")
    print("3. Quick Start with Sample Data")
    print("4. Exit")

    while True:
        match input("\nEnter your choice (1-4): ").strip():
            case "1":
                print("\n" + "=" * 50)
                print("RUNNING FULL DEMONSTRATION")
                print("=" * 50)
                run_full_demo()
            case "2":
                run_interactive_mode()
            case "3":
                print("\nQuick Start Mode - Loading sample data...")
                tracker = create_sample_data()
                run_with_sample_data(tracker)
            case "4":
                print("Goodbye!")
                sys.exit(0)
            case _:
                print("Invalid choice. Please try again.")

def run_interactive_mode():
    """Interactive mode for user input"""
    tracker = PersonalFinanceTracker()
    visualizer = FinanceVisualizer()

    while True:
        print("\n" + "=" * 50)
        print("INTERACTIVE MODE")
        print("=" * 50)
        print("1. Add Transaction")
        print("2. View Reports")
        print("3. View Visualizations")
        print("4. Set Budget")
        print("5. Check Budget Alerts")
        print("6. Export Data")
        print("7. Back to Main Menu")

        match input("\nEnter your choice (1-7): ").strip():
            case "1":
                add_transaction_interactive(tracker)
            case "2":
                view_reports_interactive(tracker)
            case "3":
                view_visualizations_interactive(tracker, visualizer)
            case "4":
                set_budget_interactive(tracker)
            case "5":
                check_budget_alerts_interactive(tracker)
            case "6":
                export_data_interactive(tracker)
            case "7":
                return
            case _:
                print("Invalid choice. Please try again.")

def add_transaction_interactive(tracker):
    """Interactive transaction addition"""
    print("\n" + "-" * 30)
    print("ADD NEW TRANSACTION")
    print("-" * 30)

    date = input("Date (YYYY-MM-DD) [Today]: ").strip()
    if not date:
        date = current_date.strftime("%Y-%m-%d")

    trans_type = ""
    while trans_type not in ['income', 'expense']:
        trans_type = input("Type (income/expense): ").strip().lower()
        if trans_type not in ['income', 'expense']:
            print("Please enter 'income' or 'expense'")

    category = input("Category: ").strip()
    description = input("Description: ").strip()

    amount = 0
    while amount <= 0:
        try:
            amount = float(input("Amount: ").strip())
            if amount <= 0:
                print("Amount must be positive")
        except ValueError:
            print("Please enter a valid number")

    payment_method = input("Payment Method [Cash]: ").strip() or "Cash"

    tracker.add_transaction(date, trans_type, category, description, amount, payment_method)
    print("✓ Transaction added successfully!")

def view_reports_interactive(tracker):
    """Interactive report viewing"""
    print("\n" + "-" * 30)
    print("GENERATE REPORT")
    print("-" * 30)

    month = input(f"Month (1-12) [{current_date.month}]: ").strip()
    year = input(f"Year (e.g., 2024) [{current_date.year}]: ").strip()

    month = int(month) if month else current_date.month
    year = int(year) if year else current_date.year

    tracker.generate_monthly_report(month, year)

def view_visualizations_interactive(tracker, visualizer):
    """Interactive visualization menu"""
    print("\n" + "-" * 30)
    print("VISUALIZATIONS")
    print("-" * 30)
    print("1. Income vs Expenses")
    print("2. Expense Categories")
    print("3. Spending Trends")
    print("4. Budget vs Actual")
    print("5. Back")

    match input("\nChoose visualization (1-5): ").strip():
        case "1":
            months = input("Number of months to show [3]: ").strip() or "3"
            try:
                visualizer.plot_income_vs_expenses(tracker, months=int(months))
            except Exception as excep:
                print(f"Error generating visualization: {excep}")
        case "2":
            month = input(f"Month (1-12) [{current_date.month}]: ").strip()
            year = input(f"Year [{current_date.year}]: ").strip()
            month = int(month) if month else current_date.month
            year = int(year) if year else current_date.year
            try:
                visualizer.plot_expense_categories(tracker, month=month, year=year)
            except Exception as excep:
                print(f"Error generating visualization: {excep}")
        case "3":
            category = input("Category (leave blank for all): ").strip() or None
            try:
                visualizer.plot_spending_trends(tracker, category=category)
            except Exception as excep:
                print(f"Error generating visualization: {excep}")
        case "4":
            month = input(f"Month (1-12) [{current_date.month}]: ").strip()
            year = input(f"Year [{current_date.year}]: ").strip()
            month = int(month) if month else current_date.month
            year = int(year) if year else current_date.year
            try:
                visualizer.plot_budget_vs_actual(tracker, month=month, year=year)
            except Exception as excep:
                print(f"Error generating visualization: {excep}")
        case "5":
            return
        case _:
            print("Invalid choice!")

def set_budget_interactive(tracker):
    """Set budget for a category"""
    print("\n" + "-" * 30)
    print("SET BUDGET")
    print("-" * 30)

    category = input("Category: ").strip()

    amount = 0
    while amount <= 0:
        try:
            amount = float(input(f"Monthly budget for {category}: $").strip())
            if amount <= 0:
                print("Amount must be positive")
        except ValueError:
            print("Please enter a valid number")

    tracker.set_budget(category, amount)

def check_budget_alerts_interactive(tracker):
    """Check budget alerts"""
    print("\n" + "-" * 30)
    print("BUDGET ALERTS")
    print("-" * 30)

    month = input(f"Month (1-12) [{current_date.month}]: ").strip()
    year = input(f"Year [{current_date.year}]: ").strip()

    month = int(month) if month else current_date.month
    year = int(year) if year else current_date.year

    alerts = tracker.check_budget_alerts(month, year)

    if alerts:
        print(f"\n⚠️ BUDGET ALERTS for {month}/{year}:")
        for alert in alerts:
            print(f"\n  Category: {alert['category']}")
            print(f"  Budget: ${alert['budget_limit']:.2f}")
            print(f"  Spent: ${alert['amount_spent']:.2f}")
            print(f"  Over by: ${alert['over_by']:.2f} ({alert['percentage_over']:.1f}%)")
    else:
        print(f"\n✓ All categories within budget for {month}/{year}!")
        print("No budgets set. Use 'Set Budget' option to create budgets.")

def export_data_interactive(tracker):
    """Export data to CSV"""
    print("\n" + "-" * 30)
    print("EXPORT DATA")
    print("-" * 30)

    filename = input("Filename [finance_data.csv]: ").strip() or "finance_data.csv"

    try:
        if not filename.endswith('.csv'):
            filename += '.csv'

        # Create data directory if it doesn't exist
        data_dir = 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        filepath = os.path.join(data_dir, filename)
        tracker.transactions.to_csv(filepath, index=False)
        print(f"✓ Data exported to {filepath}")
        print(f"✓ {len(tracker.transactions)} transactions saved")
    except Exception as excep:
        print(f"Error exporting data: {excep}")

def run_with_sample_data(tracker):
    """Run with preloaded sample data"""
    visualizer = FinanceVisualizer()

    print("\n" + "=" * 50)
    print("QUICK START MODE")
    print("=" * 50)
    print(f"✓ Sample data loaded successfully!")
    print(f"✓ {len(tracker.transactions)} transactions added")
    print(f"✓ {len(tracker.budget_limits)} budgets set")

    while True:
        print("\n" + "-" * 30)
        print("QUICK START MENU")
        print("-" * 30)
        print("1. View Monthly Report")
        print("2. View Visualizations")
        print("3. Check Budget Alerts")
        print("4. Add More Transactions")
        print("5. View All Transactions")
        print("6. Return to Main Menu")

        match input("\nEnter your choice (1-6): ").strip():
            case "1":
                month = input(f"Month (1-12) [{current_date.month}]: ").strip()
                year = input(f"Year [{current_date.year}]: ").strip()

                month = int(month) if month else current_date.month
                year = int(year) if year else current_date.year

                tracker.generate_monthly_report(month, year)
            case "2":
                view_visualizations_interactive(tracker, visualizer)
            case "3":
                check_budget_alerts_interactive(tracker)
            case "4":
                add_transaction_interactive(tracker)
            case "5":
                print("\n" + "=" * 50)
                print("ALL TRANSACTIONS")
                print("=" * 50)
                print(tracker.transactions.to_string())
            case "6":
                return
            case _:
                print("Invalid choice!")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Check if required packages are installed
    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as e:
        print(f"Error: Missing required package - {e}")
        print("Please install required packages:")
        print("pip install numpy pandas matplotlib seaborn")
        sys.exit(1)

    main()
    input("\nPress Enter to exit...")