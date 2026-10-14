import re
from datetime import datetime


class InvalidInputError(Exception):
    """Raised when a value entered by the user is not valid."""


def get_valid_date():
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            if not re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", date):
                raise InvalidInputError("Use the YYYY-MM-DD format.")
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except (InvalidInputError, ValueError) as error:
            print(f"Invalid date: {error}")


def get_valid_category():
    while True:
        category = input("Enter category: ").strip().lower()
        if category:
            return category
        print("Category cannot be empty.")


def get_valid_amount(prompt="Enter amount: "):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                raise InvalidInputError("Amount must be greater than zero.")
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")
        except InvalidInputError as error:
            print(error)


def get_valid_budget():
    while True:
        value = input("Enter spending budget (or 0 for no limit): ").strip()
        try:
            budget = float(value)
            if budget < 0:
                raise InvalidInputError("Budget cannot be negative.")
            return budget
        except ValueError:
            print("Invalid budget. Please enter a number.")
        except InvalidInputError as error:
            print(error)


def parse_tags(tag_input):
    return {
        tag.strip().lower()
        for tag in tag_input.split(",")
        if tag.strip()
    }


def generate_expense_id(expenses):
    highest_id = 0
    for expense in expenses:
        match = re.fullmatch(r"EXP-(\d{3})", str(expense.expense_id))
        if match:
            highest_id = max(highest_id, int(match.group(1)))
        elif str(expense.expense_id).isdigit():
            # Accept IDs written by earlier SpendWise versions.
            highest_id = max(highest_id, int(expense.expense_id))

    if highest_id >= 999:
        raise InvalidInputError("No IDs remain in the required EXP-001 to EXP-999 range.")
    return f"EXP-{highest_id + 1:03d}"
