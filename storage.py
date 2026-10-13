
import json
from pathlib import Path

from models import Expense


# Location of the JSON file
FILE_PATH = Path(__file__).parent / "expenses.json"


def load_expenses():
    """Load expenses from the JSON file."""
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid data format in expenses.json.")
            return []

        expenses = []

        for item in data:
            try:
                expense = Expense.from_dict(item)
                expenses.append(expense)
            except (KeyError, TypeError, ValueError) as error:
                print(f"Skipping invalid expense: {error}")

        return expenses

    except FileNotFoundError:
        # Create an empty JSON file if it does not exist
        save_expenses([])
        return []

    except json.JSONDecodeError:
        print("Warning: expenses.json contains invalid JSON.")
        return []

    except OSError as error:
        print(f"Error reading expenses: {error}")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    try:
        data = [expense.to_dict() for expense in expenses]

        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print("Expenses saved successfully.")

    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving expenses: {error}")
