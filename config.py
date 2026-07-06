import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # --- Database ---
    # Using SQLite for now so the app runs instantly with zero setup.
    # To switch to MySQL later, just set SQLALCHEMY_DATABASE_URI to something like:
    #   mysql+pymysql://username:password@localhost/bankdb
    # and add PyMySQL to requirements.txt (already included).
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'bank.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Business rules ---
    DAILY_WITHDRAWAL_LIMIT = 50000.00
    CURRENCY_SYMBOL = "₹"
