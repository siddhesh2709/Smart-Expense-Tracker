"""
models.py - Data models for the Smart Expense Tracker.

Defines the Transaction and Budget classes used throughout the application.
Demonstrates OOP concepts: classes, __init__, instance methods, class methods,
class variables, and data encapsulation.
"""

import uuid
from datetime import date, datetime
from typing import Optional


class Transaction:
    """
    Represents a single financial transaction — either an income or an expense.

    Attributes:
        id          : Unique 8-character identifier (e.g. "A3F9B21C").
        type        : "income" or "expense".
        amount      : Monetary value, stored as a float rounded to 2 decimal places.
        category    : One of the predefined category strings for the transaction type.
        description : Free-text note about the transaction.
        date        : The calendar date of the transaction (datetime.date).
    """

    # Valid transaction types
    TYPES = ("income", "expense")

    # Predefined categories for each transaction type
    CATEGORIES = {
        "income": [
            "Salary",
            "Freelance",
            "Investment",
            "Gift",
            "Other",
        ],
        "expense": [
            "Rent",
            "Food",
            "Travel",
            "Utilities",
            "Entertainment",
            "Healthcare",
            "Education",
            "Shopping",
            "Other",
        ],
    }

    def __init__(
        self,
        transaction_type: str,
        amount: float,
        category: str,
        description: str,
        transaction_date: date,
        transaction_id: Optional[str] = None,
    ):
        """
        Initialise a Transaction instance.

        Args:
            transaction_type : "income" or "expense".
            amount           : Positive monetary amount.
            category         : Category label (should match CATEGORIES).
            description      : Short description of the transaction.
            transaction_date : The date on which the transaction occurred.
            transaction_id   : Optional existing ID (used when loading from storage).

        Raises:
            ValueError: If transaction_type is not "income" or "expense".
        """
        if transaction_type not in self.TYPES:
            raise ValueError(
                f"transaction_type must be one of {self.TYPES}, got '{transaction_type}'."
            )
        self.id: str = transaction_id or str(uuid.uuid4())[:8].upper()
        self.type: str = transaction_type
        self.amount: float = round(float(amount), 2)
        self.category: str = category
        self.description: str = description
        self.date: date = transaction_date

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize the Transaction to a plain dictionary suitable for JSON storage.

        Returns:
            dict with keys: id, type, amount, category, description, date (ISO string).
        """
        return {
            "id": self.id,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat(),   # e.g. "2026-09-15"
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """
        Deserialize a Transaction from a dictionary (as loaded from JSON).

        Args:
            data: Dictionary with the same keys produced by to_dict().

        Returns:
            A new Transaction instance.
        """
        return cls(
            transaction_type=data["type"],
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            transaction_date=date.fromisoformat(data["date"]),
            transaction_id=data["id"],
        )

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id!r}, type={self.type!r}, "
            f"amount={self.amount}, category={self.category!r}, "
            f"date={self.date})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.id == other.id


class Budget:
    """
    Represents the user's monthly budget configuration.

    Attributes:
        overall_limit   : Maximum total monthly spending (0.0 = not set).
        category_limits : Dictionary mapping category name → spending limit.
    """

    def __init__(
        self,
        overall_limit: float = 0.0,
        category_limits: Optional[dict] = None,
    ):
        """
        Initialise a Budget instance.

        Args:
            overall_limit   : Overall monthly spending cap (default 0 = unset).
            category_limits : Mapping of {category: limit} (default empty).
        """
        self.overall_limit: float = round(float(overall_limit), 2)
        self.category_limits: dict = dict(category_limits) if category_limits else {}

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def set_overall(self, amount: float) -> None:
        """Set the overall monthly spending limit."""
        self.overall_limit = round(float(amount), 2)

    def set_category(self, category: str, amount: float) -> None:
        """Set a spending limit for a specific expense category."""
        self.category_limits[category] = round(float(amount), 2)

    def remove_category(self, category: str) -> None:
        """Remove a per-category spending limit (no-op if not set)."""
        self.category_limits.pop(category, None)

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialize the Budget to a plain dictionary for JSON storage."""
        return {
            "overall_limit": self.overall_limit,
            "category_limits": self.category_limits,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        """Deserialize a Budget from a dictionary (as loaded from JSON)."""
        return cls(
            overall_limit=data.get("overall_limit", 0.0),
            category_limits=data.get("category_limits", {}),
        )

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Budget(overall_limit={self.overall_limit}, "
            f"category_limits={self.category_limits})"
        )
