import re


class Expense:
    """One income or expense record stored by SpendWise."""

    def __init__(self, expense_id, date, category, amount, tags, transaction_type="expense"):
        self.expense_id = str(expense_id)
        self.date = date
        self.category = category
        self.amount = float(amount)
        self.tags = set(tags)
        self.transaction_type = transaction_type.lower()

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "tags": sorted(self.tags),
            "type": self.transaction_type,
        }

    @classmethod
    def from_dict(cls, data):
        # Convert IDs from earlier versions to the required EXP-### format.
        expense_id = str(data["expense_id"])
        if expense_id.isdigit():
            expense_id = f"EXP-{int(expense_id):03d}"
        return cls(
            expense_id,
            data["date"],
            data["category"],
            data["amount"],
            data.get("tags", []),
            data.get("type", "expense"),
        )

    def __str__(self):
        kind = self.transaction_type.title()
        return (
            f"[{self.date}] {kind} | {self.category}: ${self.amount:.2f} "
            f"(tags: {', '.join(sorted(self.tags))})"
        )


class ExpenseTracker:
    def __init__(self, expenses=None, budget_limit=0.0):
        self.expenses = expenses if expenses is not None else []
        self.budget_limit = float(budget_limit)

    def add_expense(self, expense):
        self.expenses.append(expense)

    def get_total_spending(self):
        total = 0.0
        for expense in self.expenses:
            if expense.transaction_type == "expense":
                total += expense.amount
        return total

    def get_total_income(self):
        total = 0.0
        for expense in self.expenses:
            if expense.transaction_type == "income":
                total += expense.amount
        return total

    def is_over_budget(self):
        return self.budget_limit > 0 and self.get_total_spending() > self.budget_limit

    def category_summary(self):
        category_totals = {}
        for expense in self.expenses:
            if expense.transaction_type == "expense":
                category = expense.category
                category_totals[category] = category_totals.get(category, 0.0) + expense.amount
        return category_totals

    def filter_by_category(self, category_name):
        matching_expenses = []
        for expense in self.expenses:
            if (
                expense.transaction_type == "expense"
                and expense.category.lower() == category_name.strip().lower()
            ):
                matching_expenses.append(expense)
        return matching_expenses

    def sort_by_amount(self, descending=True):
        return sorted(
            self.expenses,
            key=lambda expense: expense.amount,
            reverse=descending,
        )

    def sort_by_date(self, descending=True):
        return sorted(
            self.expenses,
            key=lambda expense: expense.date,
            reverse=descending,
        )

    def get_summary_pair(self):
        return len(self.expenses), self.get_total_spending()
