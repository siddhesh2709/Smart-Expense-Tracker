"""
transaction_manager.py - Module 1: Income and Expense Management.

Provides full CRUD (Create, Read, Update, Delete) operations for financial
transactions, including category selection, tabular display, and filtering.

Python concepts demonstrated:
    - Functions, lists, dictionaries
    - OOP (Transaction class)
    - Exception handling
    - CRUD operations
    - String formatting and terminal I/O
"""

from datetime import date
from typing import List

from src.models import Transaction
from src.validators import (
    validate_amount,
    validate_date,
    validate_non_empty,
    validate_choice,
    validate_index_choice,
)
from src.utils import (
    format_currency,
    get_input,
    pause,
    print_error,
    print_header,
    print_success,
    print_table,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _select_category(transaction_type: str) -> str:
    """
    Display available categories for the given transaction type and return
    the user's selection.

    Args:
        transaction_type: "income" or "expense".

    Returns:
        The selected category string.
    """
    categories = Transaction.CATEGORIES[transaction_type]
    print("\n  Available categories:")
    for i, cat in enumerate(categories, 1):
        print(f"    {i}. {cat}")
    idx = get_input(
        "Select category number: ",
        lambda raw: validate_index_choice(raw, len(categories)),
    )
    return categories[idx - 1]


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

def add_transaction(transactions: List[Transaction]) -> None:
    """
    Prompt the user for transaction details, validate every field, create a
    Transaction object, and append it to the in-memory list.

    Args:
        transactions: Mutable list of Transaction objects (modified in place).
    """
    print_header("ADD TRANSACTION")
    try:
        # 1. Transaction type
        t_type = get_input(
            "Type (income / expense): ",
            lambda raw: validate_choice(raw, ["income", "expense"]),
        )

        # 2. Amount
        amount = get_input("Amount (₹): ", validate_amount)

        # 3. Category  (depends on type)
        category = _select_category(t_type)

        # 4. Description
        description = get_input(
            "Description: ",
            lambda raw: validate_non_empty(raw, "Description"),
        )

        # 5. Date  (pressing Enter uses today's date)
        today_str = date.today().strftime("%d-%m-%Y")
        txn_date = get_input(
            f"Date (DD-MM-YYYY) [press Enter for today {today_str}]: ",
            lambda raw: validate_date(raw) if raw.strip() else date.today(),
        )

        txn = Transaction(
            transaction_type=t_type,
            amount=amount,
            category=category,
            description=description,
            transaction_date=txn_date,
        )
        transactions.append(txn)
        print_success(
            f"Transaction {txn.id} added — {format_currency(amount)} [{t_type.capitalize()}]"
        )

    except RuntimeError as exc:
        print_error(str(exc))

    pause()


def view_transactions(transactions: List[Transaction]) -> None:
    """
    Display transactions in a formatted table.  Supports filtering by type
    or by category.

    Args:
        transactions: List of Transaction objects to display.
    """
    print_header("VIEW TRANSACTIONS")

    if not transactions:
        print("\n  No transactions found. Add some first!")
        pause()
        return

    # Filter selection
    print("\n  Filter options:")
    print("    1. All transactions")
    print("    2. Income only")
    print("    3. Expenses only")
    print("    4. Filter by category")

    try:
        choice = get_input(
            "Select filter: ",
            lambda raw: validate_index_choice(raw, 4),
        )
    except RuntimeError as exc:
        print_error(str(exc))
        pause()
        return

    filtered = transactions[:]   # shallow copy so we don't mutate the original

    if choice == 2:
        filtered = [t for t in transactions if t.type == "income"]
    elif choice == 3:
        filtered = [t for t in transactions if t.type == "expense"]
    elif choice == 4:
        all_cats = sorted({t.category for t in transactions})
        if not all_cats:
            print("\n  No categories found.")
            pause()
            return
        print("\n  Available categories: " + ", ".join(all_cats))
        try:
            cat = get_input(
                "Enter category name: ",
                lambda raw: validate_choice(raw, all_cats),
            )
            filtered = [t for t in transactions if t.category == cat]
        except RuntimeError as exc:
            print_error(str(exc))
            pause()
            return

    if not filtered:
        print("\n  No transactions match the selected filter.")
        pause()
        return

    # Build and print the table
    headers = ["ID", "Date", "Type", "Category", "Description", "Amount"]
    rows = [
        [
            t.id,
            t.date.strftime("%d-%m-%Y"),
            t.type.capitalize(),
            t.category,
            (t.description[:24] + "…") if len(t.description) > 25 else t.description,
            format_currency(t.amount),
        ]
        for t in sorted(filtered, key=lambda x: x.date)
    ]

    print()
    print_table(headers, rows, col_widths=[10, 12, 9, 15, 26, 14])
    print(f"\n  Showing {len(filtered)} of {len(transactions)} transaction(s).")
    pause()


def edit_transaction(transactions: List[Transaction]) -> None:
    """
    Let the user select a transaction by ID and update one of its fields.

    Args:
        transactions: Mutable list of Transaction objects (modified in place).
    """
    print_header("EDIT TRANSACTION")

    if not transactions:
        print("\n  No transactions available to edit.")
        pause()
        return

    # Ask for ID
    try:
        txn_id = get_input(
            "Enter Transaction ID to edit (e.g. A3F9B21C): ",
            lambda raw: validate_non_empty(raw.strip().upper(), "Transaction ID"),
        )
    except RuntimeError as exc:
        print_error(str(exc))
        pause()
        return

    txn = next((t for t in transactions if t.id == txn_id), None)
    if txn is None:
        print_error(f"No transaction found with ID '{txn_id}'.")
        pause()
        return

    # Show current details
    print(
        f"\n  Found: [{txn.type.capitalize()}] {txn.category} — "
        f"{format_currency(txn.amount)} on {txn.date.strftime('%d-%m-%Y')}"
    )
    print(f"  Description: {txn.description}\n")

    print("  What would you like to edit?")
    print("    1. Amount")
    print("    2. Category")
    print("    3. Description")
    print("    4. Date")
    print("    5. Cancel")

    try:
        choice = get_input("Select field: ", lambda raw: validate_index_choice(raw, 5))
    except RuntimeError as exc:
        print_error(str(exc))
        pause()
        return

    try:
        if choice == 1:
            txn.amount = get_input("New amount (₹): ", validate_amount)
            print_success(f"Amount updated to {format_currency(txn.amount)}.")
        elif choice == 2:
            txn.category = _select_category(txn.type)
            print_success(f"Category updated to '{txn.category}'.")
        elif choice == 3:
            txn.description = get_input(
                "New description: ",
                lambda raw: validate_non_empty(raw, "Description"),
            )
            print_success("Description updated.")
        elif choice == 4:
            txn.date = get_input("New date (DD-MM-YYYY): ", validate_date)
            print_success(f"Date updated to {txn.date.strftime('%d-%m-%Y')}.")
        elif choice == 5:
            print("\n  Edit cancelled.")
    except RuntimeError as exc:
        print_error(str(exc))

    pause()


def delete_transaction(transactions: List[Transaction]) -> None:
    """
    Let the user delete a transaction by ID after explicit confirmation.

    Args:
        transactions: Mutable list of Transaction objects (modified in place).
    """
    print_header("DELETE TRANSACTION")

    if not transactions:
        print("\n  No transactions available to delete.")
        pause()
        return

    try:
        txn_id = get_input(
            "Enter Transaction ID to delete: ",
            lambda raw: validate_non_empty(raw.strip().upper(), "Transaction ID"),
        )
    except RuntimeError as exc:
        print_error(str(exc))
        pause()
        return

    txn = next((t for t in transactions if t.id == txn_id), None)
    if txn is None:
        print_error(f"No transaction found with ID '{txn_id}'.")
        pause()
        return

    # Show details and ask for confirmation
    print(
        f"\n  Found: [{txn.type.capitalize()}] {txn.category} — "
        f"{format_currency(txn.amount)} on {txn.date.strftime('%d-%m-%Y')}"
    )
    print(f"  Description: {txn.description}")
    confirm = input("\n  Permanently delete this transaction? (yes / no): ").strip().lower()

    if confirm in ("yes", "y"):
        transactions.remove(txn)
        print_success(f"Transaction {txn.id} has been deleted.")
    else:
        print("\n  Deletion cancelled — no changes made.")

    pause()


# ---------------------------------------------------------------------------
# Submenu
# ---------------------------------------------------------------------------

def run_transaction_menu(transactions: List[Transaction]) -> None:
    """
    Display the Income & Expense Management submenu and route the user's
    choice to the appropriate CRUD function.

    Args:
        transactions: Shared mutable list of Transaction objects.
    """
    while True:
        print_header("INCOME & EXPENSE MANAGEMENT")
        print("    1. Add Transaction")
        print("    2. View Transactions")
        print("    3. Edit Transaction")
        print("    4. Delete Transaction")
        print("    5. Back to Main Menu")

        try:
            choice = get_input(
                "Select option: ",
                lambda raw: validate_index_choice(raw, 5),
            )
        except RuntimeError:
            # Re-display the menu on repeated bad input
            continue

        if choice == 1:
            add_transaction(transactions)
        elif choice == 2:
            view_transactions(transactions)
        elif choice == 3:
            edit_transaction(transactions)
        elif choice == 4:
            delete_transaction(transactions)
        elif choice == 5:
            break
