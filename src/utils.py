"""
utils.py - Shared utility helpers for the Smart Expense Tracker.

Contains reusable functions for terminal output formatting, user input
with retry logic, and currency formatting.

Demonstrates: functions, f-strings, os module, type hints, callable parameters.
"""

import os
import uuid
from typing import Any, Callable, List


# ---------------------------------------------------------------------------
# ID generation
# ---------------------------------------------------------------------------

def generate_id() -> str:
    """
    Generate a short, unique 8-character transaction ID.

    Uses the first 8 characters of a UUID4 string, uppercased.
    Example output: "A3F9B21C"

    Returns:
        8-character uppercase hex string.
    """
    return str(uuid.uuid4())[:8].upper()


# ---------------------------------------------------------------------------
# Currency formatting
# ---------------------------------------------------------------------------

def format_currency(amount: float) -> str:
    """
    Format a float as an Indian Rupee currency string with thousands separators.

    Args:
        amount: Monetary value to format.

    Returns:
        Formatted string, e.g. "₹1,23,456.78".
    """
    # Use Python's built-in comma grouping (Western style) for simplicity.
    return f"₹{amount:,.2f}"


# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------

def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform manner."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str, width: int = 62) -> None:
    """
    Print a prominent section header with a surrounding border.

    Args:
        title : Text to display inside the header.
        width : Total width of the header border (default 62).
    """
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_success(message: str) -> None:
    """Print a success notification prefixed with a checkmark symbol."""
    print(f"\n  ✔  {message}")


def print_error(message: str) -> None:
    """Print an error notification prefixed with a cross symbol."""
    print(f"\n  ✘  Error: {message}")


def print_warning(message: str) -> None:
    """Print a warning notification prefixed with a warning symbol."""
    print(f"\n  ⚠  Warning: {message}")


def pause() -> None:
    """Pause execution and wait for the user to press Enter."""
    input("\n  Press Enter to continue...")


# ---------------------------------------------------------------------------
# Input with retry logic
# ---------------------------------------------------------------------------

def get_input(
    prompt: str,
    validator: Callable[[str], Any],
    max_attempts: int = 5,
) -> Any:
    """
    Prompt the user for input, re-prompting on validation failure.

    The validator is any callable that accepts a raw string and either returns
    a cleaned value or raises ValueError. If the user provides invalid input,
    the error message is displayed and they are prompted again.

    Args:
        prompt      : The prompt string shown before the input cursor.
        validator   : A callable(raw: str) -> Any that validates the input.
        max_attempts: Maximum number of attempts before raising RuntimeError.

    Returns:
        The cleaned value returned by the validator.

    Raises:
        RuntimeError: If the user exceeds max_attempts without valid input.
    """
    for attempt in range(max_attempts):
        raw = input(f"  {prompt}").strip()
        try:
            return validator(raw)
        except ValueError as exc:
            remaining = max_attempts - attempt - 1
            suffix = f"  ({remaining} attempt(s) left)" if remaining > 0 else ""
            print_error(f"{exc}{suffix}")

    raise RuntimeError(
        f"Too many invalid inputs after {max_attempts} attempts. Returning to menu."
    )


# ---------------------------------------------------------------------------
# Table printer
# ---------------------------------------------------------------------------

def print_table(
    headers: List[str],
    rows: List[List[Any]],
    col_widths: List[int] = None,
) -> None:
    """
    Print a formatted ASCII table to the terminal.

    Args:
        headers   : List of column header strings.
        rows      : List of rows; each row is a list of cell values.
        col_widths: Optional explicit column widths. Auto-calculated if None.
    """
    if not rows:
        # Print headers only with a separator
        col_widths = col_widths or [max(len(h), 10) for h in headers]
    elif col_widths is None:
        col_widths = [
            max(
                len(str(headers[i])),
                max(len(str(row[i])) for row in rows),
            )
            for i in range(len(headers))
        ]

    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    row_fmt   = "|" + "|".join(f" {{:<{w}}} " for w in col_widths) + "|"

    print(separator)
    print(row_fmt.format(*headers))
    print(separator)
    for row in rows:
        print(row_fmt.format(*[str(cell) for cell in row]))
    print(separator)
