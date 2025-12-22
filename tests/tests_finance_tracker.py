import pytest
from src.finance_tracker import PersonalFinanceTracker

class TestFinanceTracker:
    def setup_method(self):
        self.tracker = PersonalFinanceTracker()

    def test_add_income_transaction(self):
        self.tracker.add_transaction('2024-01-01', 'income', 'Salary', 'Monthly salary', 3000)
        assert len(self.tracker.transactions) == 1
        assert self.tracker.transactions.iloc[0]['amount'] == 3000
        assert self.tracker.transactions.iloc[0]['type'] == 'income'

    def test_add_expense_transaction(self):
        self.tracker.add_transaction('2024-01-02', 'expense', 'Food', 'Groceries', 50)
        assert len(self.tracker.transactions) == 1
        assert self.tracker.transactions.iloc[0]['type'] == 'expense'

    def test_get_summary(self):
        self.tracker.add_transaction('2024-01-01', 'income', 'Salary', 'Salary', 3000)
        self.tracker.add_transaction('2024-01-02', 'expense', 'Food', 'Groceries', 100)
        summary = self.tracker.get_financial_summary()
        assert summary['total_income'] == 3000
        assert summary['total_expenses'] == 100
        assert summary['net_savings'] == 2900

    def test_set_budget(self):
        self.tracker.set_budget('Food', 500)
        assert 'Food' in self.tracker.budget_limits
        assert self.tracker.budget_limits['Food'] == 500

if __name__ == '__main__':
    pytest.main()