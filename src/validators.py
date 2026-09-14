"""
validators.py - Input validation functions for the Smart Expense Tracker.

Each public function accepts a raw string from the user and either returns a
clean, typed value or raises ValueError with a helpful message.  No function
here interacts with the terminal directly — that responsibility belongs to
utils.get_input(), which calls these validators in a retry loop.

Demonstrates: exception handling, type conversion, string methods, datetime parsing.
"""

from datetime import date, datetime
from typing import List


def validate_amount(raw: str) -> float:
    """
    Validate and convert a monetary amount string to a positive float.

    Accepts values with or without a leading ₹ symbol and with commas
    as thousands separators (e.g. "₹1,50,000" → 150000.0).

    Args:
        raw: Raw string input from the user.

    Returns:
        Positive float amount rounded to 2 decimal places.

    Raises:
        ValueError: If the input is not a positive number.
    """
    cleaned = raw.strip().lstrip("₹").replace(",", "")
    if not cleaned:
        raise ValueError("Amount cannot be empty. Please enter a positive number.")
    try:
        amount = float(cleaned)
    except ValueError:
        raise ValueError(
            f"'{raw.strip()}' is not a valid number. "
            "Enter a value like 1500 or 1500.50."
        )
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def validate_date(raw: str) -> date:
    """
    Validate and parse a date string into a datetime.date object.

    Accepted formats:
        DD-MM-YYYY   e.g. 15-09-2026
        YYYY-MM-DD   e.g. 2026-09-15
        DD/MM/YYYY   e.g. 15/09/2026

    Args:
        raw: Raw string input from the user.

    Returns:
        A datetime.date object representing the parsed date.

    Raises:
        ValueError: If the input cannot be parsed in any accepted format.
    """
    raw = raw.strip()
    if not raw:
        raise ValueError("Date cannot be empty.")
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ValueError(
        f"'{raw}' is not a recognised date. "
        "Use DD-MM-YYYY (e.g. 15-09-2026) or YYYY-MM-DD (e.g. 2026-09-15)."
    )


def validate_non_empty(raw: str, field_name: str = "Field") -> str:
    """
    Validate that a string is not blank or whitespace-only.

    Args:
        raw        : Raw string input from the user.
        field_name : Human-readable label for error messages.

    Returns:
        Stripped, non-empty string.

    Raises:
        ValueError: If the stripped string is empty.
    """
    value = raw.strip()
    if not value:
        raise ValueError(f"{field_name} cannot be empty.")
    return value


def validate_choice(raw: str, options: List[str]) -> str:
    """
    Validate that the input matches one of the allowed option strings
    (case-insensitive comparison).

    Args:
        raw    : Raw string input from the user.
        options: List of valid option strings.

    Returns:
        The matching option string from the options list (original casing preserved).

    Raises:
        ValueError: If the input does not match any option.
    """
    raw = raw.strip()
    for opt in options:
        if opt.lower() == raw.lower():
            return opt
    raise ValueError(
        f"'{raw}' is not valid. Choose one of: {', '.join(options)}."
    )


def validate_index_choice(raw: str, max_index: int) -> int:
    """
    Validate a numeric menu selection within the range [1, max_index].

    Args:
        raw       : Raw string input from the user.
        max_index : The highest valid menu number (1-based, inclusive).

    Returns:
        Integer choice within [1, max_index].

    Raises:
        ValueError: If the input is not an integer or is out of range.
    """
    raw = raw.strip()
    try:
        choice = int(raw)
    except ValueError:
        raise ValueError(f"Please enter a number between 1 and {max_index}.")
    if not (1 <= choice <= max_index):
        raise ValueError(
            f"{choice} is out of range. Enter a number between 1 and {max_index}."
        )
    return choice
