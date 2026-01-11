import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me")
    db_url = os.environ.get("DATABASE_URL", "sqlite:///grocerflow.db")
    if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
        # Keep SQLite DB inside instance folder
        db_file = db_url.replace("sqlite:///", "")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, db_file)}"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_TIME_LIMIT"] = None

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from .auth import auth_bp
    from .routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        from .seed import ensure_default_admin
        db.create_all()
        ensure_default_admin()

    # Template helpers
    from .utils import currency
    app.jinja_env.filters["currency"] = currency

    return app
