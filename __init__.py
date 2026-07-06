from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import Config
from app.models import db, User

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.transactions import transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)

    with app.app_context():
        db.create_all()

    @app.template_filter("currency")
    def currency_filter(value):
        return f"{app.config['CURRENCY_SYMBOL']}{float(value):,.2f}"

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
