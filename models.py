from datetime import datetime
import random
import string

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """A login identity. Every account holder, employee, and admin is a User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)

    # admin | employee | customer
    role = db.Column(db.String(20), nullable=False, default="customer")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    accounts = db.relationship("Account", backref="owner", lazy=True)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Account(db.Model):
    """A bank account. A user can hold more than one (savings, current, etc.)."""

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    account_type = db.Column(db.String(20), nullable=False, default="savings")  # savings | current
    balance = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="active")  # active | frozen | closed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship(
        "Transaction",
        backref="account",
        lazy=True,
        foreign_keys="Transaction.account_id",
        order_by="Transaction.created_at.desc()",
    )

    @staticmethod
    def generate_account_number():
        while True:
            number = "".join(random.choices(string.digits, k=12))
            if not Account.query.filter_by(account_number=number).first():
                return number

    def __repr__(self):
        return f"<Account {self.account_number} bal={self.balance}>"


class Transaction(db.Model):
    """Every deposit, withdrawal, and transfer is recorded here — the audit trail
    that powers mini statements and reports."""

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False, index=True)

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)

    # For transfers, this links to the other side of the transaction.
    related_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=True)

    # deposit | withdrawal | transfer_out | transfer_in
    type = db.Column(db.String(20), nullable=False)

    amount = db.Column(db.Numeric(14, 2), nullable=False)
    balance_after = db.Column(db.Numeric(14, 2), nullable=False)

    description = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default="success")  # success | failed

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    @staticmethod
    def generate_reference():
        return "TXN" + "".join(random.choices(string.digits, k=10))

    def __repr__(self):
        return f"<Txn {self.reference} {self.type} {self.amount}>"
