# Smart Expense Tracker

A command-line personal finance management application built in Python.
Track your income and expenses, set monthly budgets, and generate financial
reports — all from your terminal.

---

## Project Overview

**Smart Expense Tracker** is a terminal-based personal finance application
developed as a Python Essentials course project.  It demonstrates core Python
programming concepts including OOP, file handling, data structures, exception
handling, and modular programming.

---

## Features

| Module | Features |
|---|---|
| **Income & Expense Management** | Add, view, edit, delete transactions; categorise income and expenses; filter by type or category |
| **Budget Management** | Set overall monthly spending limit; set per-category limits; view live budget status with warnings |
| **Financial Reports & Analysis** | Overall summary (income, expenses, balance, savings rate); category-wise breakdown; month-by-month summary |
| **Data Storage & Validation** | Persist data in JSON; load on startup; validate all inputs with helpful error messages; handle missing or corrupt files gracefully |

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.8+ | Core application language |
| `json` (stdlib) | Data serialisation and file storage |
| `uuid` (stdlib) | Unique transaction ID generation |
| `datetime` (stdlib) | Date parsing, formatting, and arithmetic |
| `collections` (stdlib) | `defaultdict` for report aggregation |
| `unittest` (stdlib) | Unit testing framework |
| `os` (stdlib) | File system path resolution |

> **No third-party libraries are required.**  The project runs on any machine with Python 3.8 or later installed.

---

## Python Version

Python **3.8 or higher** is required.

Check your version:
```bash
python --version
```

---

## Project Structure

```
smart-expense-tracker/
│
├── data/
│   ├── transactions.json      # Persisted transaction records
│   └── budget.json            # Persisted budget settings
│
├── src/
│   ├── __init__.py
│   ├── models.py              # Transaction and Budget classes (OOP)
│   ├── storage.py             # JSON file I/O (file handling)
│   ├── transaction_manager.py # Module 1: CRUD for transactions
│   ├── budget_manager.py      # Module 2: Budget setting and tracking
│   ├── report_manager.py      # Module 3: Financial reports
│   ├── validators.py          # Input validation (exception handling)
│   └── utils.py               # Shared helpers and terminal utilities
│
├── tests/
│   ├── __init__.py
│   └── test_transactions.py   # Unit tests (50+ test cases)
│
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies (stdlib only)
├── README.md                  # This file
└── statement.md               # Problem statement and project scope
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/smart-expense-tracker.git
   cd smart-expense-tracker
   ```

2. **Verify Python version**
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

3. **No packages to install** — the project uses only the Python standard library.

---

## How to Run the Application

From the project root directory:

```bash
python main.py
```

The application will display the main menu:

```
  ╔══════════════════════════════════════════════════════════════╗
  ║        SMART EXPENSE TRACKER  v1.0                          ║
  ║        Personal Finance Management System                    ║
  ║        Course: Python Essentials                             ║
  ╚══════════════════════════════════════════════════════════════╝

  Data loaded: 0 transaction(s) on record.

==============================================================
  MAIN MENU
==============================================================
    1. Income & Expense Management
    2. Budget Management
    3. Financial Reports & Analysis
    4. Save & Exit
--------------------------------------------------------------
  Select option (1-4):
```

---

## How to Test the Application

Run the full unit test suite from the project root:

```bash
python -m unittest discover tests/ -v
```

Or, if you have pytest installed:

```bash
python -m pytest tests/ -v
```

Expected output (all tests passing):

```
test_august_expenses (tests.test_transactions.TestMonthlySummary) ... ok
test_august_income (tests.test_transactions.TestMonthlySummary) ... ok
...
----------------------------------------------------------------------
Ran 50 tests in 0.XXXs

OK
```

---

## Example Input and Output

### Adding a Transaction

```
==============================================================
  ADD TRANSACTION
==============================================================
  Type (income / expense): income
  Amount (₹): 30000
  Available categories:
    1. Salary
    2. Freelance
    ...
  Select category number: 1
  Description: September salary
  Date (DD-MM-YYYY) [press Enter for today 15-09-2026]: 01-09-2026

  ✔  Transaction A3F9B21C added — ₹30,000.00 [Income]
```

### Overall Financial Summary

```
==============================================================
  OVERALL FINANCIAL SUMMARY
==============================================================
  Total Income              : ₹30,000.00
  Total Expenses            : ₹17,000.00
  Remaining Balance         : ₹13,000.00
  Savings Rate              : 43.33%

  Good. Consider increasing your savings target to 30%.
```

### Budget Status

```
==============================================================
  BUDGET STATUS — September 2026
==============================================================
  Overall Monthly Budget
  Limit             : ₹25,000.00
  Spent this month  : ₹17,000.00
  Remaining         : ₹8,000.00
  Used              : 68.0%

  Budget is under control. Keep it up!

  Category Breakdown:
+------------------+----------------+----------------+----------------+------------------+
| Category         | Spent          | Limit          | Remaining      | Status           |
+------------------+----------------+----------------+----------------+------------------+
| Food             | ₹4,000.00      | ₹5,000.00      | ₹1,000.00      | OK               |
| Rent             | ₹8,000.00      | ₹8,000.00      | ₹0.00          | !! OVER BUDGET   |
| Travel           | ₹2,000.00      | No limit       | —              | No limit         |
+------------------+----------------+----------------+----------------+------------------+
```

---

## Data Storage

- All transactions are saved to `data/transactions.json`.
- Budget settings are saved to `data/budget.json`.
- Data is saved automatically when you return from a module, and on exit.
- The `data/` directory is created automatically on first run.

---

## Non-Functional Requirements

| Requirement | Implementation |
|---|---|
| Usability | Simple numbered menu system; clear prompts and error messages |
| Reliability | Invalid inputs trigger retries (up to 5 attempts); corrupt files handled gracefully |
| Maintainability | Single-responsibility modules; fully documented with docstrings |
| Performance | O(n) data processing suitable for personal finance scale |
| Error Handling | All user inputs validated before use; exceptions caught and reported |
| Resource Efficiency | No unnecessary in-memory copies; JSON loaded once at startup |

---

## Author

Developed as a Python Essentials course project.
