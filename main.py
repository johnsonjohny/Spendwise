from models import Expense, ExpenseTracker
from storage import FILE_PATH, load_from_json, save_to_json
from utils import (
    InvalidInputError,
    generate_expense_id,
    get_valid_amount,
    get_valid_budget,
    get_valid_category,
    get_valid_date,
    parse_tags,
)


def add_new_expense(tracker):
    print("\n--- Add Transaction ---")
    transaction_type = input("Type (expense/income): ").strip().lower()
    while transaction_type not in {"expense", "income"}:
        print("Enter 'expense' or 'income'.")
        transaction_type = input("Type (expense/income): ").strip().lower()

    try:
        expense_id = generate_expense_id(tracker.expenses)
    except InvalidInputError as error:
        print(error)
        return

    date = get_valid_date()
    category = get_valid_category()
    amount = get_valid_amount("Enter amount: ")
    tags = parse_tags(input("Enter tags separated by commas: "))

    expense = Expense(
        expense_id=expense_id,
        date=date,
        category=category,
        amount=amount,
        tags=tags,
        transaction_type=transaction_type,
    )
    tracker.add_expense(expense)
    save_to_json(FILE_PATH, tracker.expenses)
    print(f"Transaction added successfully! ID: {expense_id}")
    show_budget_status(tracker)


def view_expenses(tracker):
    print("\n--- All Transactions ---")
    if not tracker.expenses:
        print("No transactions found.")
        return

    print("1. Sort by date (newest first)")
    print("2. Sort by amount (highest first)")
    choice = input("Sort option (Enter to keep saved order): ").strip()
    if choice == "1":
        expenses = tracker.sort_by_date()
    elif choice == "2":
        expenses = tracker.sort_by_amount()
    else:
        expenses = tracker.expenses

    print(f"{'ID':<9} {'DATE':<12} {'TYPE':<9} {'CATEGORY':<16} {'AMOUNT':>12}  TAGS")
    print("-" * 78)
    for expense in expenses:
        print(
            f"{expense.expense_id:<9} {expense.date:<12} "
            f"{expense.transaction_type:<9} {expense.category:<16} "
            f"${expense.amount:>11.2f}  {', '.join(sorted(expense.tags))}"
        )


def view_category_summary(tracker):
    print("\n--- Category Summary ---")
    summary = tracker.category_summary()
    if not summary:
        print("No expenses available.")
        return

    for category, amount in summary.items():
        print(f"{category.title()}: ${amount:.2f}")


def filter_expenses(tracker):
    category = get_valid_category()
    results = tracker.filter_by_category(category)
    print(f"\n--- Expenses in {category.title()} ---")
    if not results:
        print("No expenses found in this category.")
        return

    for expense in results:
        print(expense)


def show_budget_status(tracker):
    budget = tracker.budget_limit
    spending = tracker.get_total_spending()
    print(f"Spending: ${spending:.2f}")
    if budget <= 0:
        print("No spending budget is set.")
    elif tracker.is_over_budget():
        print(f"Warning: spending is over the ${budget:.2f} budget.")
    elif spending >= budget * 0.8:
        print(f"Warning: spending is approaching the ${budget:.2f} budget.")
    else:
        print(f"Budget remaining: ${budget - spending:.2f}")


def main():
    expenses = load_from_json()
    budget_limit = get_valid_budget()
    tracker = ExpenseTracker(expenses, budget_limit)

    print("Welcome to SpendWise!")
    while True:
        print("1. Add Expense")
        print("2. View All Transactions")
        print("3. View Category Summary")
        print("4. Search Expenses by Category")
        print("5. Save and Exit")
        choice = input("Enter your choice: ").strip().lower()

        match choice:
            case "1":
                add_new_expense(tracker)
            case "2":
                view_expenses(tracker)
            case "3":
                view_category_summary(tracker)
            case "4":
                filter_expenses(tracker)
            case "5" | "exit":
                save_to_json(FILE_PATH, tracker.expenses)
                print("Thank you for using SpendWise!")
                break
            case _:
                print("Invalid option! Please enter a number from 1 to 5, or 'exit'.")


if __name__ == "__main__":
    main()
