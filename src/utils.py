import pandas as pd

def export_to_csv(tracker, filename='finance_data.csv'):
    """Export transactions to CSV"""
    tracker.transactions.to_csv(filename, index=False)
    print(f"✓ Data exported to {filename}")

def import_from_csv(tracker, filename):
    """Import transactions from CSV"""
    try:
        imported_data = pd.read_csv(filename)
        tracker.transactions = pd.concat([tracker.transactions, imported_data], ignore_index=True)
        tracker.transactions['date'] = pd.to_datetime(tracker.transactions['date'])
        print(f"✓ Data imported from {filename}")
    except Exception as e:
        print(f"Error importing data: {e}")