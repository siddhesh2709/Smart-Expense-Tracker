"""
storage.py - File I/O for the Smart Expense Tracker.

Handles loading and saving of transaction and budget data using JSON files.
Paths are resolved relative to the project root so the app can be run from
any working directory.

Demonstrates: file handling, JSON serialisation, os.path, exception handling.
"""

import json
import os
from typing import List

from src.models import Transaction, Budget

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------
# __file__ is  .../smart-expense-tracker/src/storage.py
# _PROJECT_ROOT is .../smart-expense-tracker/
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSACTIONS_FILE = os.path.join(_PROJECT_ROOT, "data", "transactions.json")
BUDGET_FILE = os.path.join(_PROJECT_ROOT, "data", "budget.json")


def _ensure_data_dir() -> None:
    """Create the data/ directory if it does not already exist."""
    data_dir = os.path.join(_PROJECT_ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)


# ---------------------------------------------------------------------------
# Transaction persistence
# ---------------------------------------------------------------------------

def load_transactions() -> List[Transaction]:
    """
    Load all transactions from the JSON storage file.

    Returns an empty list if the file does not exist or is corrupted,
    printing a warning to the user rather than crashing the application.

    Returns:
        List of Transaction objects.
    """
    _ensure_data_dir()
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    try:
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return []
            data = json.loads(raw)
        return [Transaction.from_dict(item) for item in data]
    except json.JSONDecodeError as e:
        print(f"  [Warning] transactions.json is corrupted: {e}. Starting with empty list.")
        return []
    except (KeyError, ValueError) as e:
        print(f"  [Warning] Could not parse a transaction record: {e}. Starting with empty list.")
        return []


def save_transactions(transactions: List[Transaction]) -> None:
    """
    Save the current list of transactions to the JSON storage file.

    Args:
        transactions: List of Transaction objects to persist.
    """
    _ensure_data_dir()
    data = [t.to_dict() for t in transactions]
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Budget persistence
# ---------------------------------------------------------------------------

def load_budget() -> Budget:
    """
    Load budget settings from the JSON storage file.

    Returns a default Budget (no limits set) if the file does not exist
    or cannot be parsed.

    Returns:
        Budget object with stored or default settings.
    """
    _ensure_data_dir()
    if not os.path.exists(BUDGET_FILE):
        return Budget()
    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return Budget()
            data = json.loads(raw)
        return Budget.from_dict(data)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"  [Warning] budget.json could not be loaded: {e}. Using default budget.")
        return Budget()


def save_budget(budget: Budget) -> None:
    """
    Save budget settings to the JSON storage file.

    Args:
        budget: Budget object to persist.
    """
    _ensure_data_dir()
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budget.to_dict(), f, indent=2, ensure_ascii=False)
