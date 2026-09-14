"""
budget_manager.py - Module 2: Budget Management.

Allows the user to set a monthly overall spending limit and per-category
limits, and then view a live status report that highlights budget warnings.

Python concepts demonstrated:
    - Conditional statements (if/elif/else)
    - Functions and argument passing
    - Dictionaries and set operations
    - Calculations and percentage formatting
    - File handling (delegated to storage.py)
"""

from datetime import date
from typing import Dict, List

from src.models import Budget, Transaction
from src.validators import validate_amount, validate_index_choice
from src.utils import (
    format_currency,
    get_input,
    pause,
    print_error,
    print_header,
    print_success,
    print_table,
    print_warning,
)


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _expenses_this_month(transactions: List[Transaction]) -> Dict[str, float]:
    """
    Aggregate expense amounts by category for the current calendar month.

    Only expense-type transactions whose date falls in the current year and
    month are included.

    Args:
        transactions: Full list of all transactions.

    Returns:
        Dict mapping category name → total amount spent this month.
    """
    today = date.today()
    totals: Dict[str, float] = {}
    for t in transactions:
        if (
            t.type == "expense"
            and t.date.year == today.year
            and t.date.month == today.month
        ):
            totals[t.category] = round(totals.get(t.category, 0.0) + t.amount, 2)
    return totals


# ---------------------------------------------------------------------------
# Budget operations
# ---------------------------------------------------------------------------

def set_budget(budget: Budget) -> None:
    """
    Interactive menu to add or remove budget limits.

    Options:
        1. Set overall monthly spending limit.
        2. Set a per-category spending limit.
        3. Remove a per-category limit.
        4. Return to the budget menu.

    Args:
        budget: Budget object (modified in place).
    """
    print_header("SET BUDGET")
    print("    1. Set overall monthly spending limit")
    print("    2. Set per-category spending limit")
    print("    3. Remove a category limit")
    print("    4. Back")

    try:
        choice = get_input(
            "Select option: ",
            lambda raw: validate_index_choice(raw, 4),
        )
    except RuntimeError as exc:
        print_error(str(exc))
        pause()
        return

    if choice == 1:
        # ── Overall limit ──────────────────────────────────────────────────
        try:
            limit = get_input("Overall monthly limit (₹): ", validate_amount)
            budget.set_overall(limit)
            print_success(f"Overall monthly budget set to {format_currency(limit)}.")
        except RuntimeError as exc:
            print_error(str(exc))

    elif choice == 2:
        # ── Per-category limit ─────────────────────────────────────────────
        cats = Transaction.CATEGORIES["expense"]
        print("\n  Expense categories:")
        for i, c in enumerate(cats, 1):
            current = budget.category_limits.get(c)
            tag = f"  (current: {format_currency(current)})" if current else ""
            print(f"    {i}. {c}{tag}")
        try:
            idx = get_input(
                "Select category: ",
                lambda raw: validate_index_choice(raw, len(cats)),
            )
            cat = cats[idx - 1]
            limit = get_input(f"Monthly limit for '{cat}' (₹): ", validate_amount)
            budget.set_category(cat, limit)
            print_success(f"Budget for '{cat}' set to {format_currency(limit)}.")
        except RuntimeError as exc:
            print_error(str(exc))

    elif choice == 3:
        # ── Remove a category limit ────────────────────────────────────────
        if not budget.category_limits:
            print("\n  No per-category limits have been set yet.")
        else:
            cat_list = list(budget.category_limits.keys())
            print("\n  Current category limits:")
            for i, c in enumerate(cat_list, 1):
                print(f"    {i}. {c} — {format_currency(budget.category_limits[c])}")
            try:
                idx = get_input(
                    "Select category to remove: ",
                    lambda raw: validate_index_choice(raw, len(cat_list)),
                )
                cat = cat_list[idx - 1]
                budget.remove_category(cat)
                print_success(f"Category limit for '{cat}' removed.")
            except RuntimeError as exc:
                print_error(str(exc))

    # choice == 4: just return silently
    pause()


def view_budget_status(transactions: List[Transaction], budget: Budget) -> None:
    """
    Display a comprehensive budget status report for the current calendar month.

    Shows:
        - Overall budget limit vs. total monthly spending.
        - Per-category breakdown with spent/limit/remaining/status columns.
        - Budget warnings when spending reaches 80 % or 100 % of a limit.

    Args:
        transactions: Full list of all transactions.
        budget       : Current budget settings.
    """
    month_label = date.today().strftime("%B %Y")
    print_header(f"BUDGET STATUS — {month_label}")

    spent_by_cat = _expenses_this_month(transactions)
    total_spent  = round(sum(spent_by_cat.values()), 2)

    # ── Overall budget ─────────────────────────────────────────────────────
    if budget.overall_limit > 0:
        remaining = round(budget.overall_limit - total_spent, 2)
        pct       = (total_spent / budget.overall_limit) * 100

        print(f"\n  Overall Monthly Budget")
        print(f"  {'Limit':<18}: {format_currency(budget.overall_limit)}")
        print(f"  {'Spent this month':<18}: {format_currency(total_spent)}")
        print(f"  {'Remaining':<18}: {format_currency(remaining)}")
        print(f"  {'Used':<18}: {pct:.1f}%")

        if pct >= 100:
            print_warning("You have EXCEEDED your monthly budget!")
        elif pct >= 80:
            print_warning(
                f"You have used {pct:.1f}% of your monthly budget. Spend carefully!"
            )
        else:
            print(f"\n  Budget is under control. Keep it up!")
    else:
        print(f"\n  Total spent this month : {format_currency(total_spent)}")
        print(
            "  No overall monthly budget set.\n"
            "  Go to 'Set Budget' to add one."
        )

    # ── Per-category breakdown ─────────────────────────────────────────────
    all_categories = sorted(
        set(spent_by_cat.keys()) | set(budget.category_limits.keys())
    )
    if all_categories:
        print("\n  Category Breakdown:")
        headers = ["Category", "Spent", "Limit", "Remaining", "Status"]
        rows = []
        for cat in all_categories:
            spent = spent_by_cat.get(cat, 0.0)
            limit = budget.category_limits.get(cat)
            if limit:
                remaining = round(limit - spent, 2)
                pct       = (spent / limit) * 100
                if pct >= 100:
                    status = "!! OVER BUDGET"
                elif pct >= 80:
                    status = "! WARNING"
                else:
                    status = "OK"
                rows.append(
                    [cat, format_currency(spent), format_currency(limit),
                     format_currency(remaining), status]
                )
            else:
                rows.append(
                    [cat, format_currency(spent), "No limit", "—", "No limit"]
                )
        print()
        print_table(headers, rows, col_widths=[16, 14, 14, 14, 16])

    pause()


# ---------------------------------------------------------------------------
# Submenu
# ---------------------------------------------------------------------------

def run_budget_menu(transactions: List[Transaction], budget: Budget) -> None:
    """
    Display the Budget Management submenu and route choices to the
    appropriate functions.

    Args:
        transactions: Shared list of Transaction objects.
        budget       : Shared Budget object (modified in place).
    """
    while True:
        print_header("BUDGET MANAGEMENT")
        print("    1. Set Budget Limits")
        print("    2. View Budget Status (Current Month)")
        print("    3. Back to Main Menu")

        try:
            choice = get_input(
                "Select option: ",
                lambda raw: validate_index_choice(raw, 3),
            )
        except RuntimeError:
            continue

        if choice == 1:
            set_budget(budget)
        elif choice == 2:
            view_budget_status(transactions, budget)
        elif choice == 3:
            break
