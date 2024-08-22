from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()  # Initialize SQLAlchemy outside of the create_app function
migrate = Migrate()  # Initialize Migrate outside of the create_app function
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"  # Consider using environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)  # Initialize SQLAlchemy with the app
    migrate.init_app(app, db)  # Initialize Migrate with the app and db

    # Register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import models
    from .models import User, Post, Comment, Like

    # Create the database if it does not exist
    create_database(app)

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # Ensure the directory for the database file exists
    if not path.exists("website/"):
        makedirs("website/")
    
    if not path.exists("website/" + DB_NAME):
        with app.app_context():  # Ensure app context is active
            db.create_all()
        print("Created database!")
