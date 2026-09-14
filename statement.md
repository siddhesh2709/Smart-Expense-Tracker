# Statement of Purpose

## Project Title

Smart Expense Tracker – A Python-Based Personal Finance Management System

---

## Problem Statement

Managing personal finances is a fundamental life skill, yet many individuals
— especially students and young professionals — lack accessible tools to track
their income and spending habits.  Commercial applications are often complex,
subscription-based, or require an internet connection.

This project addresses that gap by providing a simple, self-contained,
command-line personal finance management system that any user can run on their
own computer with no account, no installation of third-party software, and no
connectivity required.

---

## Project Scope

The scope of this project is limited to:

- A **command-line interface (CLI)** application; no graphical or web interface.
- **Single-user** operation on a local machine.
- Data stored **locally** in JSON files; no databases or cloud services.
- Transaction records consisting of **income** and **expense** entries only.
  Investment portfolio tracking, loan management, and tax calculations are
  explicitly out of scope.
- **Monthly budgeting** against predefined expense categories.
- Financial reports covering the **full history** of stored transactions and
  broken down by calendar month.

---

## Target Users

| User Group | Description |
|---|---|
| Students | Track pocket money, part-time income, and daily expenses |
| Young professionals | Monitor salary, rent, utilities, and discretionary spending |
| Anyone learning Python | Study a real-world OOP and file-handling project |
| Educators | Use as a teaching example for modular Python programming |

The application requires no financial background to use; the menu-driven
interface guides the user through every action.

---

## High-Level Features

### Module 1 — Income and Expense Management
- Add income and expense transactions with category, description, and date.
- View all transactions in a formatted table with filter options (all, income,
  expense, or by category).
- Edit any field of an existing transaction by its unique ID.
- Delete a transaction with a confirmation prompt to prevent accidental loss.

### Module 2 — Budget Management
- Set an overall monthly spending limit.
- Set individual limits per expense category (e.g. Food, Rent, Travel).
- View a live budget status report showing how much has been spent and how much
  remains for the current calendar month.
- Automatic warnings when spending reaches 80 % and 100 % of any limit.

### Module 3 — Financial Reports and Analysis
- **Overall Summary**: total income, total expenses, remaining balance, and
  savings rate as a percentage.
- **Category Breakdown**: expense totals per category ranked by spend, with
  percentage share of total expenses.
- **Monthly Summary**: income, expenses, and balance grouped by calendar month,
  sorted chronologically.

### Module 4 — Data Storage and Validation
- Persist all transactions and budget settings to local JSON files.
- Load saved data automatically on application startup.
- Validate every user input before processing:
  - Amounts must be positive numbers.
  - Dates are accepted in DD-MM-YYYY, YYYY-MM-DD, or DD/MM/YYYY format.
  - Text fields must not be empty.
  - Menu choices must be valid integers within the displayed range.
- Gracefully handle missing, empty, or corrupt data files without crashing.
- Provide up to five retry attempts for invalid inputs before returning to menu.

---

## Technologies and Python Concepts

| Concept | Where Demonstrated |
|---|---|
| Object-Oriented Programming | `Transaction` and `Budget` classes in `models.py` |
| Functions | All modules; every operation is encapsulated in a named function |
| Lists and Dictionaries | Transaction storage, category aggregation, monthly grouping |
| File Handling | `storage.py` — reading and writing JSON files |
| Exception Handling | `validators.py`, `utils.get_input()` — try/except blocks |
| Conditional Statements | Budget warnings, savings rate advice, filter logic |
| Loops | Menu loops, data aggregation loops, input retry loops |
| Modular Programming | Eight separate modules each with a single responsibility |
| `datetime` module | Date parsing and month-based grouping |
| `uuid` module | Unique transaction ID generation |
| `json` module | Data serialisation and deserialisation |
| `unittest` module | 50+ automated unit tests in `tests/test_transactions.py` |

---

## Data Model

### Transaction
| Field | Type | Description |
|---|---|---|
| id | str | Unique 8-character ID (e.g. "A3F9B21C") |
| type | str | "income" or "expense" |
| amount | float | Positive monetary amount (₹) |
| category | str | Predefined category label |
| description | str | Free-text note |
| date | date | Transaction date (stored as ISO string) |

### Budget
| Field | Type | Description |
|---|---|---|
| overall_limit | float | Total monthly spending cap (0 = not set) |
| category_limits | dict | Maps category name → spending limit |

---

## Non-Functional Requirements

| Requirement | Description |
|---|---|
| Usability | Simple, numbered menu interface requiring no technical knowledge |
| Reliability | Invalid inputs are caught and re-prompted; corrupt files do not crash the app |
| Maintainability | Each module has a single responsibility and full docstring documentation |
| Performance | All operations complete in under 1 second for typical personal finance data volumes |
| Error Handling | All user inputs validated; exceptions reported with user-friendly messages |
| Resource Efficiency | Data loaded once at startup; no unnecessary copies or open file handles |
