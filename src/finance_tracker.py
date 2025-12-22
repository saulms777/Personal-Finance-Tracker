import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class PersonalFinanceTracker:
    def __init__(self):
        self.transactions = pd.DataFrame(columns=[
            'date', 'type', 'category', 'description', 'amount', 'payment_method'
        ])
        self.categories = {
            'income': ['Salary', 'Freelance', 'Investment', 'Gift', 'Other Income'],
            'expense': ['Food', 'Transportation', 'Housing', 'Entertainment',
                        'Healthcare', 'Education', 'Shopping', 'Utilities', 'Other']
        }
        self.budget_limits = {}

    def add_transaction(self, date, trans_type, category, description, amount, payment_method='Cash'):
        """Add a new transaction to the tracker"""
        if trans_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")

        new_transaction = pd.DataFrame([{
            'date': pd.to_datetime(date),
            'type': trans_type,
            'category': category,
            'description': description,
            'amount': amount,
            'payment_method': payment_method
        }])

        self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
        print(f"✓ Added {trans_type}: {description} - ${amount:.2f}")

    def set_budget(self, category, monthly_limit):
        """Set monthly budget for a category"""
        self.budget_limits[category] = monthly_limit
        print(f"✓ Budget set for {category}: ${monthly_limit:.2f} per month")

    def get_financial_summary(self, start_date=None, end_date=None):
        """Get comprehensive financial summary for a period"""
        if start_date:
            start_date = pd.to_datetime(start_date)
        if end_date:
            end_date = pd.to_datetime(end_date)

        # Filter transactions by date range
        mask = pd.Series([True] * len(self.transactions))
        if start_date is not None:
            mask = mask & (self.transactions['date'] >= start_date)
        if end_date is not None:
            mask = mask & (self.transactions['date'] <= end_date)

        filtered_transactions = self.transactions[mask].copy()

        if len(filtered_transactions) == 0:
            print("No transactions in the specified period")
            return None

        # Calculate summary statistics
        income = filtered_transactions[filtered_transactions['type'] == 'income']['amount'].sum()
        expenses = filtered_transactions[filtered_transactions['type'] == 'expense']['amount'].sum()
        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0

        summary = {
            'total_income': income,
            'total_expenses': expenses,
            'net_savings': savings,
            'savings_rate': savings_rate,
            'avg_daily_expense': expenses / len(filtered_transactions['date'].dt.date.unique())
            if len(filtered_transactions['date'].dt.date.unique()) > 0 else 0,
            'transaction_count': len(filtered_transactions)
        }

        return summary

    def get_category_analysis(self, start_date=None, end_date=None):
        """Analyze spending/income by category"""
        if len(self.transactions) == 0:
            print("No transactions to analyze")
            return None

        # Filter by date if provided
        transactions = self.transactions
        if start_date or end_date:
            start_date = pd.to_datetime(start_date) if start_date else pd.Timestamp.min
            end_date = pd.to_datetime(end_date) if end_date else pd.Timestamp.max
            transactions = transactions[(transactions['date'] >= start_date) & (transactions['date'] <= end_date)]

        # Group by type and category
        income_by_category = transactions[transactions['type'] == 'income'] \
            .groupby('category')['amount'].sum()
        expense_by_category = transactions[transactions['type'] == 'expense'] \
            .groupby('category')['amount'].sum()

        return {
            'income_by_category': income_by_category,
            'expense_by_category': expense_by_category
        }

    def check_budget_alerts(self, month=None, year=None):
        """Check if any categories are over budget"""
        alerts = []

        if not self.budget_limits:
            print("No budgets set. Use set_budget() to create budgets.")
            return alerts

        # Determine date range
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        start_date = pd.Timestamp(year=year, month=month, day=1)
        if month == 12:
            end_date = pd.Timestamp(year=year+1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = pd.Timestamp(year=year, month=month+1, day=1) - timedelta(days=1)

        # Get expenses for the month
        monthly_expenses = self.transactions[
            (self.transactions['date'] >= start_date) &
            (self.transactions['date'] <= end_date) &
            (self.transactions['type'] == 'expense')
            ]

        # Check each budget category
        expense_by_category = monthly_expenses.groupby('category')['amount'].sum()

        for category, limit in self.budget_limits.items():
            spent = expense_by_category.get(category, 0)
            if spent > limit:
                alerts.append({
                    'category': category,
                    'budget_limit': limit,
                    'amount_spent': spent,
                    'over_by': spent - limit,
                    'percentage_over': ((spent - limit) / limit * 100)
                })

        return alerts

    def generate_monthly_report(self, month=None, year=None):
        """Generate comprehensive monthly report"""
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        print(f"\n{'=' * 50}")
        print(f"FINANCIAL REPORT - {month}/{year}")
        print(f"{'=' * 50}")

        # Get summary
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        summary = self.get_financial_summary(start_date, end_date)

        if summary:
            print(f"\nSUMMARY:")
            print(f"  Total Income:    ${summary['total_income']:.2f}")
            print(f"  Total Expenses:  ${summary['total_expenses']:.2f}")
            print(f"  Net Savings:     ${summary['net_savings']:.2f}")
            print(f"  Savings Rate:    {summary['savings_rate']:.1f}%")
            print(f"  Avg Daily Spend: ${summary['avg_daily_expense']:.2f}")

        # Category analysis
        cat_analysis = self.get_category_analysis(start_date, end_date)
        if cat_analysis:
            print(f"\nINCOME BY CATEGORY:")
            for category, amount in cat_analysis['income_by_category'].items():
                print(f"  {category}: ${amount:.2f}")

            print(f"\nEXPENSES BY CATEGORY:")
            for category, amount in cat_analysis['expense_by_category'].items():
                print(f"  {category}: ${amount:.2f}")

        # Budget alerts
        alerts = self.check_budget_alerts(month, year)
        if alerts:
            print(f"\n⚠️  BUDGET ALERTS:")
            for alert in alerts:
                print(f"  {alert['category']}: Over budget by ${alert['over_by']:.2f} "
                      f"({alert['percentage_over']:.1f}%)")

        print(f"{'=' * 50}")