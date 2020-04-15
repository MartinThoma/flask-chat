# Core Library modules
import os

# Third party modules
from flask import Flask
from flask_migrate import Migrate
from flask_restplus import Api

migrate = Migrate()
api_base = Api(version="1.0", doc="/swagger/")


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = "689ceeef-9525-4721-be8d-4ff192910eb5"
    current_directory = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_directory, "database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from .main import main as main_blueprint
    from .api import api_v1
    from .models import db

    app.register_blueprint(main_blueprint)
    db.init_app(app)
    migrate.init_app(app, db)
    api_base.add_namespace(api_v1)
    api_base.init_app(app)

    return app
