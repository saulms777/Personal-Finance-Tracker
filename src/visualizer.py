import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class FinanceVisualizer:
    @staticmethod
    def plot_income_vs_expenses(tracker, months=3):
        """Plot income vs expenses over time"""
        if len(tracker.transactions) == 0:
            print("No data to visualize")
            return

        # Prepare data
        df = tracker.transactions.copy()
        df['month'] = df['date'].dt.to_period('M')
        monthly_data = df.groupby(['month', 'type'])['amount'].sum().unstack().fillna(0)

        # Get last N months
        monthly_data = monthly_data.tail(months)

        # Plot
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))

        # Bar plot
        monthly_data[['income', 'expense']].plot(kind='bar', ax=ax[0])
        ax[0].set_title('Monthly Income vs Expenses')
        ax[0].set_ylabel('Amount ($)')
        ax[0].legend(['Income', 'Expenses'])
        ax[0].tick_params(axis='x', rotation=45)

        # Line plot for net savings
        monthly_data['net'] = monthly_data.get('income', 0) - monthly_data.get('expense', 0)
        monthly_data['net'].plot(kind='line', marker='o', ax=ax[1], color='green')
        ax[1].set_title('Monthly Net Savings')
        ax[1].set_ylabel('Net Savings ($)')
        ax[1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax[1].fill_between(range(len(monthly_data)),
                           monthly_data['net'],
                           where=(monthly_data['net'] > 0),
                           color='green', alpha=0.3)
        ax[1].fill_between(range(len(monthly_data)),
                           monthly_data['net'],
                           where=(monthly_data['net'] < 0),
                           color='red', alpha=0.3)
        ax[1].tick_params(axis='x', rotation=45)
        ax[1].set_xticks(range(len(monthly_data)))
        ax[1].set_xticklabels([str(m) for m in monthly_data.index])

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_expense_categories(tracker, month=None, year=None):
        """Visualize expense distribution by category"""
        if len(tracker.transactions) == 0:
            print("No data to visualize")
            return

        # Filter by month if specified
        df = tracker.transactions.copy()
        if month and year:
            df = df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]

        expenses = df[df['type'] == 'expense']

        if len(expenses) == 0:
            print("No expense data for the specified period")
            return

        # Group by category
        expense_by_cat = expenses.groupby('category')['amount'].sum()

        # Create subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Pie chart
        if len(expense_by_cat) > 0:
            expense_by_cat.plot(kind='pie', autopct='%1.1f%%', ax=axes[0])
            axes[0].set_title('Expense Distribution by Category')
            axes[0].set_ylabel('')

        # Bar chart (sorted)
        expense_by_cat.sort_values(ascending=False).plot(kind='bar', ax=axes[1])
        axes[1].set_title('Expenses by Category')
        axes[1].set_ylabel('Amount ($)')
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_spending_trends(tracker, category=None):
        """Plot spending trends over time"""
        if len(tracker.transactions) == 0:
            print("No data to visualize")
            return

        df = tracker.transactions.copy()
        expenses = df[df['type'] == 'expense']

        if len(expenses) == 0:
            print("No expense data")
            return

        # Convert amount to float and handle any conversion errors
        expenses['amount'] = expenses['amount'].astype(float)

        # Group by month and optionally category
        expenses['month'] = expenses['date'].dt.to_period('M')

        if category:
            category_expenses = expenses[expenses['category'] == category]
            if len(category_expenses) == 0:
                print(f"No data for category: {category}")
                return
            monthly_trend = category_expenses.groupby('month')['amount'].sum()
            title = f'Monthly Spending Trend: {category}'
        else:
            monthly_trend = expenses.groupby('month')['amount'].sum()
            title = 'Total Monthly Spending Trend'

        # Convert Period index to string for plotting
        months_str = [str(m) for m in monthly_trend.index]

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(months_str, monthly_trend.values, marker='o', linewidth=2)
        plt.title(title)
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        # Add trend line if we have enough points
        if len(monthly_trend) >= 2:
            try:
                x = np.arange(len(monthly_trend))
                y = monthly_trend.values.astype(float)
                if not np.any(np.isnan(y)):  # Check for NaN values
                    z = np.polyfit(x, y, 1)
                    p = np.poly1d(z)
                    plt.plot(x, p(x), "r--", alpha=0.5, label='Trend Line')
                    plt.legend()
            except Exception as e:
                print(f"Note: Could not calculate trend line: {e}")

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_budget_vs_actual(tracker, month=None, year=None):
        """Compare budget vs actual spending"""
        if not tracker.budget_limits:
            print("No budgets set")
            return

        # Get actual spending for the month
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        start_date = pd.Timestamp(year=year, month=month, day=1)
        if month == 12:
            end_date = pd.Timestamp(year=year+1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = pd.Timestamp(year=year, month=month+1, day=1) - timedelta(days=1)

        monthly_expenses = tracker.transactions[
            (tracker.transactions['date'] >= start_date) &
            (tracker.transactions['date'] <= end_date) &
            (tracker.transactions['type'] == 'expense')
            ]

        actual_by_category = monthly_expenses.groupby('category')['amount'].sum()

        # Prepare data for plotting
        categories = list(tracker.budget_limits.keys())
        budget_values = [tracker.budget_limits[cat] for cat in categories]
        actual_values = [actual_by_category.get(cat, 0) for cat in categories]

        # Create DataFrame for plotting
        plot_data = pd.DataFrame({
            'Category': categories,
            'Budget': budget_values,
            'Actual': actual_values
        })

        # Plot
        x = np.arange(len(categories))
        width = 0.35

        plt.figure(figsize=(12, 6))
        plt.bar(x - width/2, plot_data['Budget'], width, label='Budget', color='lightblue')
        plt.bar(x + width/2, plot_data['Actual'], width, label='Actual', color='salmon')

        # Highlight over-budget categories
        for i, (budget, actual) in enumerate(zip(budget_values, actual_values)):
            if actual > budget:
                plt.text(i, actual, f"+${actual-budget:.0f}",
                         ha='center', va='bottom', color='red', fontweight='bold')

        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.title(f'Budget vs Actual Spending - {month}/{year}')
        plt.xticks(x, categories, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()