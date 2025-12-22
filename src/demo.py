# Remove the relative import dots since we're running from main.py
from finance_tracker import PersonalFinanceTracker
from visualizer import FinanceVisualizer

def run_full_demo():
    """Run the complete demonstration"""
    print("🚀 PERSONAL FINANCE TRACKER DEMONSTRATION\n")

    # Initialize tracker
    tracker = PersonalFinanceTracker()
    visualizer = FinanceVisualizer()

    # Add sample transactions
    print("Adding sample transactions...")

    # Income transactions
    tracker.add_transaction('2024-01-05', 'income', 'Salary', 'Monthly Salary', 3500)
    tracker.add_transaction('2024-01-10', 'income', 'Freelance', 'Web design project', 800)
    tracker.add_transaction('2024-01-20', 'income', 'Investment', 'Dividend payout', 150)

    # Expense transactions
    tracker.add_transaction('2024-01-02', 'expense', 'Food', 'Grocery shopping', 120)
    tracker.add_transaction('2024-01-03', 'expense', 'Transportation', 'Gas', 60)
    tracker.add_transaction('2024-01-05', 'expense', 'Housing', 'Rent', 1200)
    tracker.add_transaction('2024-01-08', 'expense', 'Entertainment', 'Movie tickets', 40)
    tracker.add_transaction('2024-01-12', 'expense', 'Food', 'Restaurant dinner', 85)
    tracker.add_transaction('2024-01-15', 'expense', 'Shopping', 'New clothes', 120)
    tracker.add_transaction('2024-01-18', 'expense', 'Utilities', 'Electricity bill', 95)
    tracker.add_transaction('2024-01-22', 'expense', 'Healthcare', 'Doctor visit', 75)
    tracker.add_transaction('2024-01-25', 'expense', 'Food', 'Groceries', 110)
    tracker.add_transaction('2024-01-28', 'expense', 'Entertainment', 'Concert tickets', 120)

    # Add more transactions for February
    tracker.add_transaction('2024-02-05', 'income', 'Salary', 'Monthly Salary', 3500)
    tracker.add_transaction('2024-02-10', 'expense', 'Food', 'Grocery shopping', 130)
    tracker.add_transaction('2024-02-12', 'expense', 'Shopping', 'Electronics', 350)
    tracker.add_transaction('2024-02-15', 'expense', 'Housing', 'Rent', 1200)
    tracker.add_transaction('2024-02-20', 'expense', 'Transportation', 'Car maintenance', 200)

    print("\n" + "=" * 50)

    # Set budgets
    print("\nSetting budgets...")
    tracker.set_budget('Food', 300)
    tracker.set_budget('Shopping', 200)
    tracker.set_budget('Entertainment', 150)
    tracker.set_budget('Transportation', 100)

    print("\n" + "=" * 50)

    # Generate reports
    tracker.generate_monthly_report(1, 2024)
    tracker.generate_monthly_report(2, 2024)

    print("\n" + "=" * 50)

    # Get overall summary
    print("\nOVERALL FINANCIAL SUMMARY (Jan-Feb 2024):")
    summary = tracker.get_financial_summary('2024-01-01', '2024-02-28')
    if summary:
        for key, value in summary.items():
            if isinstance(value, (int, float)):
                print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\n" + "=" * 50)

    # Check budget alerts
    print("\nCHECKING BUDGET ALERTS:")
    alerts = tracker.check_budget_alerts(2, 2024)
    if alerts:
        for alert in alerts:
            print(f"  ⚠️  {alert['category']}: Spent ${alert['amount_spent']:.2f} "
                  f"(Budget: ${alert['budget_limit']:.2f})")
    else:
        print("  ✓ All categories within budget!")

    print("\n" + "=" * 50)

    # Visualizations
    print("\n📊 GENERATING VISUALIZATIONS...")

    # Plot 1: Income vs Expenses
    print("\n1. Income vs Expenses (Last 2 Months)")
    visualizer.plot_income_vs_expenses(tracker, months=2)

    # Plot 2: Expense Categories
    print("\n2. Expense Categories (January 2024)")
    visualizer.plot_expense_categories(tracker, month=1, year=2024)

    # Plot 3: Spending Trends
    print("\n3. Spending Trends (Food Category)")
    visualizer.plot_spending_trends(tracker, category='Food')

    # Plot 4: Budget vs Actual
    print("\n4. Budget vs Actual Spending (February 2024)")
    visualizer.plot_budget_vs_actual(tracker, month=2, year=2024)

    # Additional Analysis
    print("\n" + "=" * 50)
    print("\nADDITIONAL ANALYSIS:")

    # Category analysis
    cat_analysis = tracker.get_category_analysis('2024-01-01', '2024-02-28')
    if cat_analysis:
        total_expenses = cat_analysis['expense_by_category'].sum()
        print(f"\nTop 3 Expense Categories (Jan-Feb 2024):")
        top_categories = cat_analysis['expense_by_category'].sort_values(ascending=False).head(3)
        for category, amount in top_categories.items():
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            print(f"  {category}: ${amount:.2f} ({percentage:.1f}%)")

    return tracker

def create_sample_data():
    """Create and return a tracker with sample data"""
    tracker = PersonalFinanceTracker()

    # Sample data
    sample_transactions = [
        ('2024-01-05', 'income', 'Salary', 'Monthly Salary', 3500, 'Bank Transfer'),
        ('2024-01-10', 'income', 'Freelance', 'Web design', 800, 'PayPal'),
        ('2024-01-15', 'expense', 'Food', 'Groceries', 120, 'Credit Card'),
        ('2024-01-20', 'expense', 'Housing', 'Rent', 1200, 'Bank Transfer'),
        ('2024-01-25', 'expense', 'Entertainment', 'Movie', 40, 'Cash'),
        ('2024-02-05', 'income', 'Salary', 'Monthly Salary', 3500, 'Bank Transfer'),
        ('2024-02-10', 'expense', 'Food', 'Restaurant', 85, 'Credit Card'),
        ('2024-02-15', 'expense', 'Shopping', 'Clothes', 120, 'Credit Card'),
        ('2024-02-20', 'expense', 'Transportation', 'Gas', 60, 'Debit Card'),
    ]

    for transaction in sample_transactions:
        tracker.add_transaction(*transaction)

    # Set some budgets
    tracker.set_budget('Food', 300)
    tracker.set_budget('Shopping', 200)
    tracker.set_budget('Entertainment', 150)

    return tracker

if __name__ == "__main__":
    # This allows you to run the demo directly
    tracker = run_full_demo()
    input("\nPress Enter to exit...")