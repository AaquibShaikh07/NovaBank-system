"""
Run once to populate the database with a demo admin account and a couple of
sample customers with transaction history, so the dashboard has data to show.

Usage:
    python seed.py
"""
from decimal import Decimal
from datetime import datetime, timedelta
import random

from app import create_app
from app.models import db, User, Account, Transaction


def run():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(full_name="Bank Admin", email="admin@novabank.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

        customers_data = [
            ("Aditi Sharma", "aditi@example.com", "customer123"),
            ("Rohan Mehta", "rohan@example.com", "customer123"),
        ]

        accounts = []
        for name, email, pw in customers_data:
            user = User(full_name=name, email=email, role="customer")
            user.set_password(pw)
            db.session.add(user)
            db.session.flush()

            account = Account(
                account_number=Account.generate_account_number(),
                user_id=user.id,
                account_type="savings",
                balance=Decimal("0"),
            )
            db.session.add(account)
            db.session.flush()
            accounts.append(account)

        db.session.commit()

        # Give each account some transaction history over the past 6 months.
        for account in accounts:
            balance = Decimal("0")
            for i in range(20):
                days_ago = random.randint(0, 180)
                created_at = datetime.utcnow() - timedelta(days=days_ago)
                ttype = random.choice(["deposit", "deposit", "withdrawal"])
                amount = Decimal(random.choice([500, 1000, 2500, 5000, 10000]))

                if ttype == "withdrawal":
                    amount = min(amount, balance) if balance > 0 else Decimal("0")
                    if amount == 0:
                        continue
                    balance -= amount
                else:
                    balance += amount

                txn = Transaction(
                    reference=Transaction.generate_reference(),
                    account_id=account.id,
                    type=ttype,
                    amount=amount,
                    balance_after=balance,
                    description="Sample seed transaction",
                    created_at=created_at,
                )
                db.session.add(txn)

            account.balance = balance

        db.session.commit()
        print("Database seeded successfully.")
        print("Admin login:    admin@novabank.com / admin123")
        print("Customer login: aditi@example.com / customer123")
        print("Customer login: rohan@example.com / customer123")


if __name__ == "__main__":
    run()
