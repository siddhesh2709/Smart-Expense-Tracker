"""
test_transactions.py - Unit tests for the Smart Expense Tracker.

Tests cover:
    - Input validation functions  (validators.py)
    - Transaction and Budget model classes  (models.py)
    - Financial report calculation functions  (report_manager.py)

Run the full test suite from the project root with:
    python -m unittest discover tests/
or, if pytest is installed:
    python -m pytest tests/ -v
"""

import unittest
from datetime import date

from src.models import Transaction, Budget
from src.validators import (
    validate_amount,
    validate_choice,
    validate_date,
    validate_index_choice,
    validate_non_empty,
)
from src.report_manager import calculate_summary, category_breakdown, monthly_summary


# =============================================================================
# 1. Validator Tests
# =============================================================================

class TestValidateAmount(unittest.TestCase):
    """Tests for validators.validate_amount()."""

    def test_integer_string(self):
        self.assertEqual(validate_amount("1500"), 1500.0)

    def test_float_string(self):
        self.assertEqual(validate_amount("1234.50"), 1234.50)

    def test_strips_rupee_symbol(self):
        self.assertEqual(validate_amount("₹2000"), 2000.0)

    def test_strips_commas(self):
        self.assertEqual(validate_amount("1,50,000"), 150000.0)

    def test_strips_rupee_and_commas(self):
        self.assertEqual(validate_amount("₹1,50,000.50"), 150000.50)

    def test_whitespace_stripped(self):
        self.assertEqual(validate_amount("  500  "), 500.0)

    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            validate_amount("0")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            validate_amount("-500")

    def test_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            validate_amount("abc")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            validate_amount("")

    def test_rounding(self):
        # Should round to 2 decimal places
        self.assertEqual(validate_amount("99.999"), 100.0)


class TestValidateDate(unittest.TestCase):
    """Tests for validators.validate_date()."""

    def test_dd_mm_yyyy_format(self):
        self.assertEqual(validate_date("15-09-2026"), date(2026, 9, 15))

    def test_yyyy_mm_dd_format(self):
        self.assertEqual(validate_date("2026-09-15"), date(2026, 9, 15))

    def test_dd_slash_mm_slash_yyyy_format(self):
        self.assertEqual(validate_date("15/09/2026"), date(2026, 9, 15))

    def test_leading_trailing_whitespace(self):
        self.assertEqual(validate_date("  15-09-2026  "), date(2026, 9, 15))

    def test_invalid_format_raises(self):
        with self.assertRaises(ValueError):
            validate_date("09-15-2026")   # US format not supported

    def test_nonsense_string_raises(self):
        with self.assertRaises(ValueError):
            validate_date("not-a-date")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            validate_date("")


class TestValidateNonEmpty(unittest.TestCase):
    """Tests for validators.validate_non_empty()."""

    def test_valid_string_returned_stripped(self):
        self.assertEqual(validate_non_empty("  Hello  ", "Field"), "Hello")

    def test_non_empty_string(self):
        self.assertEqual(validate_non_empty("Description", "Field"), "Description")

    def test_whitespace_only_raises(self):
        with self.assertRaises(ValueError):
            validate_non_empty("   ", "Field")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            validate_non_empty("", "Field")


class TestValidateChoice(unittest.TestCase):
    """Tests for validators.validate_choice()."""

    def test_exact_match(self):
        self.assertEqual(validate_choice("income", ["income", "expense"]), "income")

    def test_case_insensitive_upper(self):
        self.assertEqual(validate_choice("INCOME", ["income", "expense"]), "income")

    def test_case_insensitive_mixed(self):
        self.assertEqual(validate_choice("Expense", ["income", "expense"]), "expense")

    def test_invalid_option_raises(self):
        with self.assertRaises(ValueError):
            validate_choice("savings", ["income", "expense"])

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            validate_choice("", ["income", "expense"])


class TestValidateIndexChoice(unittest.TestCase):
    """Tests for validators.validate_index_choice()."""

    def test_valid_lower_bound(self):
        self.assertEqual(validate_index_choice("1", 5), 1)

    def test_valid_upper_bound(self):
        self.assertEqual(validate_index_choice("5", 5), 5)

    def test_middle_value(self):
        self.assertEqual(validate_index_choice("3", 5), 3)

    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            validate_index_choice("0", 5)

    def test_above_max_raises(self):
        with self.assertRaises(ValueError):
            validate_index_choice("6", 5)

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            validate_index_choice("abc", 5)


# =============================================================================
# 2. Transaction Model Tests
# =============================================================================

class TestTransactionModel(unittest.TestCase):
    """Tests for the Transaction class in models.py."""

    def _make(self, t_type="expense", amount=500.0, category="Food",
              description="Lunch", txn_date=None):
        """Helper to create a Transaction with sensible defaults."""
        return Transaction(
            transaction_type=t_type,
            amount=amount,
            category=category,
            description=description,
            transaction_date=txn_date or date(2026, 9, 15),
        )

    def test_creation_stores_fields(self):
        txn = self._make(amount=750.0, category="Travel")
        self.assertEqual(txn.type, "expense")
        self.assertEqual(txn.amount, 750.0)
        self.assertEqual(txn.category, "Travel")

    def test_id_auto_generated(self):
        txn = self._make()
        self.assertIsNotNone(txn.id)
        self.assertEqual(len(txn.id), 8)
        self.assertTrue(txn.id.isupper())

    def test_custom_id_preserved(self):
        txn = Transaction(
            transaction_type="income",
            amount=1000,
            category="Salary",
            description="Pay",
            transaction_date=date(2026, 9, 1),
            transaction_id="MYID1234",
        )
        self.assertEqual(txn.id, "MYID1234")

    def test_amount_rounded_to_two_decimals(self):
        txn = self._make(amount=1234.5678)
        self.assertEqual(txn.amount, 1234.57)

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            Transaction(
                transaction_type="savings",
                amount=100,
                category="Other",
                description="Test",
                transaction_date=date(2026, 9, 1),
            )

    def test_to_dict_has_required_keys(self):
        txn = self._make()
        d = txn.to_dict()
        for key in ("id", "type", "amount", "category", "description", "date"):
            self.assertIn(key, d)

    def test_to_dict_date_is_iso_string(self):
        txn = self._make(txn_date=date(2026, 9, 15))
        self.assertEqual(txn.to_dict()["date"], "2026-09-15")

    def test_from_dict_roundtrip(self):
        txn1 = self._make(amount=999.99)
        txn2 = Transaction.from_dict(txn1.to_dict())
        self.assertEqual(txn1.id, txn2.id)
        self.assertEqual(txn1.amount, txn2.amount)
        self.assertEqual(txn1.category, txn2.category)
        self.assertEqual(txn1.date, txn2.date)

    def test_equality_by_id(self):
        txn1 = self._make()
        txn2 = Transaction.from_dict(txn1.to_dict())
        self.assertEqual(txn1, txn2)


# =============================================================================
# 3. Budget Model Tests
# =============================================================================

class TestBudgetModel(unittest.TestCase):
    """Tests for the Budget class in models.py."""

    def test_default_values(self):
        b = Budget()
        self.assertEqual(b.overall_limit, 0.0)
        self.assertEqual(b.category_limits, {})

    def test_set_overall(self):
        b = Budget()
        b.set_overall(15000)
        self.assertEqual(b.overall_limit, 15000.0)

    def test_set_category(self):
        b = Budget()
        b.set_category("Food", 4000)
        self.assertEqual(b.category_limits["Food"], 4000.0)

    def test_remove_category(self):
        b = Budget(category_limits={"Food": 4000, "Rent": 8000})
        b.remove_category("Food")
        self.assertNotIn("Food", b.category_limits)
        self.assertIn("Rent", b.category_limits)

    def test_remove_nonexistent_category_no_error(self):
        b = Budget()
        # Should not raise any exception
        b.remove_category("NonExistent")

    def test_roundtrip_serialisation(self):
        b1 = Budget(overall_limit=20000, category_limits={"Rent": 8000, "Food": 4000})
        b2 = Budget.from_dict(b1.to_dict())
        self.assertEqual(b1.overall_limit, b2.overall_limit)
        self.assertEqual(b1.category_limits, b2.category_limits)


# =============================================================================
# 4. Report Manager Tests
# =============================================================================

class TestCalculateSummary(unittest.TestCase):
    """Tests for report_manager.calculate_summary()."""

    def setUp(self):
        """
        Sample transaction set matching the project example:
            Income:   ₹30,000 (Salary) + ₹5,000 (Freelance) = ₹35,000
            Expenses: ₹8,000 + ₹4,000 + ₹2,000 + ₹3,000 + ₹1,500 = ₹18,500
            Balance:  ₹16,500
        """
        self.txns = [
            Transaction("income",  30000, "Salary",    "September salary",  date(2026, 9, 1)),
            Transaction("income",   5000, "Freelance", "Project payment",   date(2026, 8, 20)),
            Transaction("expense",  8000, "Rent",      "Monthly rent",      date(2026, 9, 2)),
            Transaction("expense",  4000, "Food",      "Groceries",         date(2026, 9, 5)),
            Transaction("expense",  2000, "Travel",    "Commute",           date(2026, 9, 10)),
            Transaction("expense",  3000, "Other",     "Miscellaneous",     date(2026, 9, 15)),
            Transaction("expense",  1500, "Food",      "Dining out",        date(2026, 8, 25)),
        ]

    def test_total_income(self):
        s = calculate_summary(self.txns)
        self.assertAlmostEqual(s["total_income"], 35000.0)

    def test_total_expenses(self):
        s = calculate_summary(self.txns)
        self.assertAlmostEqual(s["total_expenses"], 18500.0)

    def test_balance(self):
        s = calculate_summary(self.txns)
        self.assertAlmostEqual(s["balance"], 16500.0)

    def test_savings_rate(self):
        s = calculate_summary(self.txns)
        expected = round((16500 / 35000) * 100, 2)
        self.assertAlmostEqual(s["savings_rate"], expected)

    def test_empty_list(self):
        s = calculate_summary([])
        self.assertEqual(s["total_income"], 0.0)
        self.assertEqual(s["total_expenses"], 0.0)
        self.assertEqual(s["balance"], 0.0)
        self.assertEqual(s["savings_rate"], 0.0)

    def test_income_only(self):
        txns = [Transaction("income", 10000, "Salary", "Pay", date(2026, 9, 1))]
        s = calculate_summary(txns)
        self.assertEqual(s["total_expenses"], 0.0)
        self.assertEqual(s["balance"], 10000.0)
        self.assertEqual(s["savings_rate"], 100.0)

    def test_expenses_exceed_income(self):
        txns = [
            Transaction("income",  1000, "Salary",  "Pay",  date(2026, 9, 1)),
            Transaction("expense", 2000, "Rent",    "Rent", date(2026, 9, 2)),
        ]
        s = calculate_summary(txns)
        self.assertLess(s["balance"], 0)


class TestCategoryBreakdown(unittest.TestCase):
    """Tests for report_manager.category_breakdown()."""

    def setUp(self):
        self.txns = [
            Transaction("income",  30000, "Salary",  "Pay",       date(2026, 9, 1)),
            Transaction("expense",  8000, "Rent",    "Rent",      date(2026, 9, 2)),
            Transaction("expense",  4000, "Food",    "Groceries", date(2026, 9, 5)),
            Transaction("expense",  1500, "Food",    "Dining",    date(2026, 8, 25)),
            Transaction("expense",  2000, "Travel",  "Commute",   date(2026, 9, 10)),
        ]

    def test_income_excluded(self):
        bd = category_breakdown(self.txns)
        self.assertNotIn("Salary", bd)

    def test_food_total(self):
        bd = category_breakdown(self.txns)
        self.assertAlmostEqual(bd["Food"], 5500.0)

    def test_rent_total(self):
        bd = category_breakdown(self.txns)
        self.assertAlmostEqual(bd["Rent"], 8000.0)

    def test_sorted_descending(self):
        bd = category_breakdown(self.txns)
        amounts = list(bd.values())
        self.assertEqual(amounts, sorted(amounts, reverse=True))

    def test_empty_list_returns_empty_dict(self):
        bd = category_breakdown([])
        self.assertEqual(bd, {})


class TestMonthlySummary(unittest.TestCase):
    """Tests for report_manager.monthly_summary()."""

    def setUp(self):
        self.txns = [
            Transaction("income",  30000, "Salary",  "Sep salary", date(2026, 9, 1)),
            Transaction("expense",  8000, "Rent",    "Rent",        date(2026, 9, 2)),
            Transaction("expense",  4000, "Food",    "Groceries",   date(2026, 9, 5)),
            Transaction("expense",  2000, "Travel",  "Commute",     date(2026, 9, 10)),
            Transaction("expense",  3000, "Other",   "Misc",        date(2026, 9, 15)),
            Transaction("income",   5000, "Freelance","Project",    date(2026, 8, 20)),
            Transaction("expense",  1500, "Food",    "Dining",      date(2026, 8, 25)),
        ]

    def test_months_present(self):
        s = monthly_summary(self.txns)
        self.assertIn("2026-09", s)
        self.assertIn("2026-08", s)

    def test_september_income(self):
        s = monthly_summary(self.txns)
        self.assertAlmostEqual(s["2026-09"]["income"], 30000.0)

    def test_september_expenses(self):
        s = monthly_summary(self.txns)
        self.assertAlmostEqual(s["2026-09"]["expenses"], 17000.0)

    def test_september_balance(self):
        s = monthly_summary(self.txns)
        self.assertAlmostEqual(s["2026-09"]["balance"], 13000.0)

    def test_august_income(self):
        s = monthly_summary(self.txns)
        self.assertAlmostEqual(s["2026-08"]["income"], 5000.0)

    def test_august_expenses(self):
        s = monthly_summary(self.txns)
        self.assertAlmostEqual(s["2026-08"]["expenses"], 1500.0)

    def test_months_sorted_chronologically(self):
        s = monthly_summary(self.txns)
        keys = list(s.keys())
        self.assertEqual(keys, sorted(keys))

    def test_empty_list_returns_empty_dict(self):
        s = monthly_summary([])
        self.assertEqual(s, {})

    def test_balance_equals_income_minus_expenses(self):
        s = monthly_summary(self.txns)
        for month, data in s.items():
            expected = round(data["income"] - data["expenses"], 2)
            self.assertAlmostEqual(data["balance"], expected, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
