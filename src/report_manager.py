"""
report_manager.py - Module 3: Financial Reports and Analysis.

Provides three types of report:
    1. Overall financial summary  (income, expenses, balance, savings rate)
    2. Category-wise expense breakdown  (sorted by spend, with share %)
    3. Monthly summary  (income, expenses, balance grouped by YYYY-MM)

Python concepts demonstrated:
    - Loops (for loops, comprehensions)
    - Dictionaries and defaultdict
    - Sorting with key functions
    - Data processing and aggregation
    - String formatting and f-strings
"""

from collections import defaultdict
from datetime import date
from typing import Dict, List

from src.models import Transaction
from src.validators import validate_index_choice
from src.utils import (
    format_currency,
    get_input,
    pause,
    print_error,
    print_header,
    print_table,
)


# ---------------------------------------------------------------------------
# Core calculation functions  (pure — no terminal I/O, fully testable)
# ---------------------------------------------------------------------------

def calculate_summary(transactions: List[Transaction]) -> Dict[str, float]:
    """
    Compute overall financial summary statistics across all transactions.

    Args:
        transactions: List of all Transaction objects.

    Returns:
        Dictionary with keys:
            total_income    : Sum of all income amounts.
            total_expenses  : Sum of all expense amounts.
            balance         : total_income − total_expenses.
            savings_rate    : balance / total_income × 100 (0 if no income).
    """
    total_income   = sum(t.amount for t in transactions if t.type == "income")
    total_expenses = sum(t.amount for t in transactions if t.type == "expense")
    balance        = total_income - total_expenses
    savings_rate   = (balance / total_income * 100) if total_income > 0 else 0.0

    return {
        "total_income":   round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance":        round(balance, 2),
        "savings_rate":   round(savings_rate, 2),
    }


def category_breakdown(transactions: List[Transaction]) -> Dict[str, float]:
    """
    Aggregate expense amounts by category, sorted from highest to lowest.

    Income transactions are excluded.

    Args:
        transactions: List of all Transaction objects.

    Returns:
        Ordered dict mapping category name → total expense amount,
        sorted in descending order of amount.
    """
    totals: Dict[str, float] = defaultdict(float)
    for t in transactions:
        if t.type == "expense":
            totals[t.category] += t.amount

    # Sort by descending spend
    return dict(
        sorted(totals.items(), key=lambda item: item[1], reverse=True)
    )


def monthly_summary(transactions: List[Transaction]) -> Dict[str, Dict[str, float]]:
    """
    Group transactions by calendar month and compute per-month statistics.

    Args:
        transactions: List of all Transaction objects.

    Returns:
        Ordered dict mapping "YYYY-MM" strings → dict with keys:
            income   : Total income for the month.
            expenses : Total expenses for the month.
            balance  : income − expenses.
        Months are sorted chronologically (oldest first).
    """
    months: Dict[str, Dict[str, float]] = defaultdict(
        lambda: {"income": 0.0, "expenses": 0.0}
    )
    for t in transactions:
        key = t.date.strftime("%Y-%m")
        if t.type == "income":
            months[key]["income"] += t.amount
        else:
            months[key]["expenses"] += t.amount

    result: Dict[str, Dict[str, float]] = {}
    for month in sorted(months.keys()):
        data    = months[month]
        balance = data["income"] - data["expenses"]
        result[month] = {
            "income":   round(data["income"],   2),
            "expenses": round(data["expenses"], 2),
            "balance":  round(balance,           2),
        }
    return result


# ---------------------------------------------------------------------------
# Report display functions
# ---------------------------------------------------------------------------

def _print_overall_summary(transactions: List[Transaction]) -> None:
    """Print the overall financial summary report to the terminal."""
    print_header("OVERALL FINANCIAL SUMMARY")

    if not transactions:
        print("\n  No transactions on record. Add some to see a summary.")
        pause()
        return

    s = calculate_summary(transactions)

    print(f"\n  {'Total Income':<26}: {format_currency(s['total_income'])}")
    print(f"  {'Total Expenses':<26}: {format_currency(s['total_expenses'])}")
    print(f"  {'Remaining Balance':<26}: {format_currency(s['balance'])}")
    print(f"  {'Savings Rate':<26}: {s['savings_rate']:.2f}%")

    # Contextual advice
    print()
    if s["balance"] < 0:
        print("  !! Your expenses exceed your income. Review your spending immediately.")
    elif s["savings_rate"] >= 30:
        print("  Excellent! You are saving over 30% of your income.")
    elif s["savings_rate"] >= 10:
        print("  Good. Consider increasing your savings target to 30%.")
    else:
        print("  Your savings rate is low. Look for areas to reduce spending.")

    pause()


def _print_category_breakdown(transactions: List[Transaction]) -> None:
    """Print a category-wise expense breakdown table."""
    print_header("CATEGORY-WISE EXPENSE BREAKDOWN")

    breakdown = category_breakdown(transactions)
    if not breakdown:
        print("\n  No expense records found.")
        pause()
        return

    total  = sum(breakdown.values())
    headers = ["Category", "Amount Spent", "Share (%)"]
    rows = [
        [
            cat,
            format_currency(amt),
            f"{(amt / total * 100):.1f}%",
        ]
        for cat, amt in breakdown.items()
    ]
    print()
    print_table(headers, rows, col_widths=[20, 16, 12])
    print(f"\n  Total Expenses : {format_currency(total)}")
    pause()


def _print_monthly_summary(transactions: List[Transaction]) -> None:
    """Print a month-wise income, expense, and balance report."""
    print_header("MONTHLY SUMMARY")

    summary = monthly_summary(transactions)
    if not summary:
        print("\n  No transactions found.")
        pause()
        return

    headers = ["Month", "Income", "Expenses", "Balance"]
    rows = [
        [
            month,
            format_currency(data["income"]),
            format_currency(data["expenses"]),
            format_currency(data["balance"]),
        ]
        for month, data in summary.items()
    ]
    print()
    print_table(headers, rows, col_widths=[12, 16, 16, 16])
    pause()


# ---------------------------------------------------------------------------
# Submenu
# ---------------------------------------------------------------------------

def run_report_menu(transactions: List[Transaction]) -> None:
    """
    Display the Financial Reports & Analysis submenu and route choices to
    the appropriate report function.

    Args:
        transactions: Shared list of Transaction objects.
    """
    while True:
        print_header("FINANCIAL REPORTS & ANALYSIS")
        print("    1. Overall Financial Summary")
        print("    2. Category-wise Expense Breakdown")
        print("    3. Monthly Summary")
        print("    4. Back to Main Menu")

        try:
            choice = get_input(
                "Select option: ",
                lambda raw: validate_index_choice(raw, 4),
            )
        except RuntimeError:
            continue

        if choice == 1:
            _print_overall_summary(transactions)
        elif choice == 2:
            _print_category_breakdown(transactions)
        elif choice == 3:
            _print_monthly_summary(transactions)
        elif choice == 4:
            break
