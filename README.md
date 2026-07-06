# NovaBank — Core Transaction Module

A working Flask + SQLAlchemy banking app covering **authentication, role-based
dashboards, and the full transaction flow**: deposit, withdraw, transfer, mini
statements, and printable receipts.

This is the first slice of a larger banking system build — solid and fully
functional, ready to extend with more modules (loans, ATM simulator, KYC,
reports, etc.) next.

## What's included

- **Auth**: register, login, logout, password hashing (Flask-Bcrypt), session
  management via Flask-Login
- **Roles**: `admin`, `employee`, `customer` (role stored on the `User` model —
  admin/employee currently share one dashboard view; easy to split later)
- **Accounts**: auto-opened savings account on registration, unique 12-digit
  account numbers
- **Transactions**:
  - Deposit (with account-status validation)
  - Withdraw (balance + daily withdrawal limit validation)
  - Transfer (atomic debit/credit across two accounts, by account number)
  - Mini statement (paginated, 15 per page)
  - Printable transaction receipt
- **Admin dashboard**: total customers, total accounts, total deposits,
  Chart.js bar chart of deposits vs. withdrawals over the last 6 months,
  recent transactions across the whole bank
- **Customer dashboard**: account balance cards, quick actions, recent activity
- **UI**: Bootstrap 5, Font Awesome, Poppins font, blue/white banking theme,
  fixed sidebar, sticky navbar, rounded cards, toast-style flash messages,
  responsive layout

## Project structure

```
bankapp/
├── app/
│   ├── __init__.py          # app factory
│   ├── models.py            # User, Account, Transaction
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   └── transactions.py
│   ├── templates/
│   └── static/css/style.css
├── config.py
├── run.py
├── seed.py                  # creates demo admin + 2 customers with history
├── requirements.txt
└── instance/bank.db         # SQLite database (created automatically)
```

## Setup

```bash
cd bankapp
pip install -r requirements.txt

# Optional: populate with demo data (admin + 2 customers, 6 months of
# sample transactions). This WIPES and recreates the database.
python seed.py

python run.py
```

Visit **http://127.0.0.1:5000**

### Demo logins (after running `seed.py`)

| Role     | Email                  | Password     |
|----------|-------------------------|--------------|
| Admin    | admin@novabank.com      | admin123     |
| Customer | aditi@example.com       | customer123  |
| Customer | rohan@example.com       | customer123  |

If you skip `seed.py`, just register a new account from the login page — it
opens a savings account automatically with a ₹0 balance.

## Switching to MySQL later

The app runs on SQLite by default (zero setup). To point it at MySQL instead:

1. `pip install pymysql` (already in requirements.txt)
2. Set an environment variable before running:
   ```bash
   export DATABASE_URL="mysql+pymysql://username:password@localhost/bankdb"
   ```
3. Create the `bankdb` database in MySQL, then run `python seed.py` (or let
   `db.create_all()` build the empty tables on first run).

No code changes needed — `config.py` reads `DATABASE_URL` if it's set.

## Known limits of this slice (by design — this is step 1)

- Employee role currently sees the same dashboard as admin (no separate
  permissions yet)
- No KYC/document upload, loans, ATM simulator, or PDF/Excel export yet
- No CSRF token on forms yet (add Flask-WTF before any real deployment)
- No OTP/email verification flow yet

Happy to build any of these next — just say which module.
