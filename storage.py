import json
from pathlib import Path

from models import Expense


FILE_PATH = Path(__file__).parent / "expenses.json"


def load_from_json(filename=FILE_PATH):
    """Load Expense objects from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid data format in expenses.json.")
            return []

        expenses = []
        for item in data:
            try:
                expenses.append(Expense.from_dict(item))
            except (KeyError, TypeError, ValueError) as error:
                print(f"Skipping invalid expense: {error}")
        return expenses

    except FileNotFoundError:
        # Create the data file so the next save has a ready destination.
        save_to_json(filename, [])
        return []
    except json.JSONDecodeError:
        print("Warning: expenses.json contains invalid JSON.")
        return []
    except OSError as error:
        print(f"Error reading expenses: {error}")
        return []


def save_to_json(filename, expenses_list):
    """Convert Expense objects to dictionaries and write them as JSON."""
    try:
        data = [expense.to_dict() for expense in expenses_list]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("Expenses saved successfully.")
    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving expenses: {error}")


# Keep these names available for projects using the original functions.
def load_expenses():
    return load_from_json()


def save_expenses(expenses):
    save_to_json(FILE_PATH, expenses)
