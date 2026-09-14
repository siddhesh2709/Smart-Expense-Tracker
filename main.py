"""
main.py - Entry point for the Smart Expense Tracker.

Loads persisted data, displays the main menu, and routes the user to each
of the four functional modules.  Data is auto-saved whenever the user returns
from a module that modifies transactions or budget settings.

Usage:
    python main.py
"""

from src.storage import load_budget, load_transactions, save_budget, save_transactions
from src.budget_manager import run_budget_menu
from src.report_manager import run_report_menu
from src.transaction_manager import run_transaction_menu
from src.utils import get_input, print_success
from src.validators import validate_index_choice


BANNER = r"""
  ╔══════════════════════════════════════════════════════════════╗
  ║        SMART EXPENSE TRACKER  v1.0                          ║
  ║        Personal Finance Management System                    ║
  ║        Course: Python Essentials                             ║
  ╚══════════════════════════════════════════════════════════════╝
"""


def main() -> None:
    """
    Application entry point.

    Loads saved transactions and budget on startup, then presents the main
    menu in a loop until the user selects Exit.
    """
    # ── Load persisted data ────────────────────────────────────────────────
    transactions = load_transactions()
    budget       = load_budget()

    print(BANNER)
    print(f"  Data loaded: {len(transactions)} transaction(s) on record.\n")

    # ── Main menu loop ─────────────────────────────────────────────────────
    while True:
        print("\n" + "=" * 62)
        print("  MAIN MENU")
        print("=" * 62)
        print("    1. Income & Expense Management")
        print("    2. Budget Management")
        print("    3. Financial Reports & Analysis")
        print("    4. Save & Exit")
        print("-" * 62)

        try:
            choice = get_input(
                "Select option (1-4): ",
                lambda raw: validate_index_choice(raw, 4),
            )
        except RuntimeError:
            # Re-display menu if user keeps entering bad input
            continue

        if choice == 1:
            run_transaction_menu(transactions)
            # Auto-save after the module exits so no data is lost
            save_transactions(transactions)

        elif choice == 2:
            run_budget_menu(transactions, budget)
            save_budget(budget)

        elif choice == 3:
            # Reports are read-only — no save needed
            run_report_menu(transactions)

        elif choice == 4:
            # Final save before exit
            save_transactions(transactions)
            save_budget(budget)
            print_success("All data saved. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
