
import re
from datetime import datetime

from models import Expense, ExpenseTracker
from storage import load_expenses, save_expenses
from utils import parse_tags, get_valid_amount


def get_valid_date():
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()

        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            print("Invalid format. Use YYYY-MM-DD.")
            continue

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date. Please try again.")


def get_valid_category():
    while True:
        category = input("Enter category: ").strip().lower()

        if category:
            return category

        print("Category cannot be empty.")



def add_new_expense(tracker):
    # Add a new expense
    print("\n--- Add Expense ---")

    # Automatically generate a simple ID
    if tracker.expenses:
        expense_id = max(int(e.expense_id) for e in tracker.expenses) + 1
    else:
        expense_id = 1

    date = get_valid_date()
    category = get_valid_category()
    amount = get_valid_amount()
    tags = parse_tags(input("Enter tags separated by commas: "))

    expense = Expense(
        expense_id=str(expense_id),
        date=date,
        category=category,
        amount=amount,
        tags=tags
    )

    tracker.add_expense(expense)
    save_expenses(tracker.expenses)

    print(f"Expense added successfully! ID: {expense_id}")


def view_expenses(tracker):
    """Display all expenses."""
    print("\n--- All Expenses ---")

    if not tracker.expenses:
        print("No expenses found.")
        return

    for expense in tracker.expenses:
        print(expense)


def view_total_spending(tracker):
    """Display total spending."""
    total = tracker.get_total_spending()
    print(f"\nTotal spending: ₹{total:.2f}")


def check_budget(tracker):
    """Check whether spending exceeds the budget."""
    print(f"\nBudget limit: ₹{tracker.budget_limit:.2f}")
    total = tracker.get_total_spending()
    print(f"Total spending: ₹{total:.2f}")

    if tracker.is_over_budget():
        print("Warning: You have exceeded your budget!")
    else:
        remaining = tracker.budget_limit - total
        print(f"Remaining budget: ₹{remaining:.2f}")


def view_category_summary(tracker):
    """Display spending grouped by category."""
    print("\n--- Category Summary ---")

    summary = tracker.category_summary()

    if not summary:
        print("No expenses available.")
        return

    for category, amount in summary.items():
        print(f"{category.title()}: ₹{amount:.2f}")


def filter_expenses(tracker):
    """Filter expenses by category."""
    category = get_valid_category()
    results = tracker.filter_by_category(category)

    print(f"\n--- Expenses in {category.title()} ---")

    if not results:
        print("No expenses found in this category.")
        return

    for expense in results:
        print(expense)


def sort_expenses(tracker):
    """Sort expenses by amount or date."""
    print("\n1. Sort by amount")
    print("2. Sort by date")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        results = tracker.sort_by_amount()
    elif choice == "2":
        results = tracker.sort_by_date()
    else:
        print("Invalid choice.")
        return

    print("\n--- Sorted Expenses ---")

    for expense in results:
        print(expense)


def main():
    """Run the SpendWise application."""
    expenses = load_expenses()
    tracker = ExpenseTracker(expenses)

    print("Welcome to SpendWise!")

    while True:
        print("\n========== SPENDWISE ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. Check Budget")
        print("5. Category Summary")
        print("6. Filter by Category")
        print("7. Sort Expenses")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                add_new_expense(tracker)

            case "2":
                view_expenses(tracker)

            case "3":
                view_total_spending(tracker)

            case "4":
                check_budget(tracker)

            case "5":
                view_category_summary(tracker)

            case "6":
                filter_expenses(tracker)

            case "7":
                sort_expenses(tracker)

            case "8":
                save_expenses(tracker.expenses)
                print("Thank you for using SpendWise!")
                break

            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
