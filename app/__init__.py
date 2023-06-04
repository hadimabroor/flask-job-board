from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secrets import token_urlsafe
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = token_urlsafe(16)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

    db.init_app(app)

    from .auth import auth
    app.register_blueprint(auth)

    from .views import views
    app.register_blueprint(views)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        

    if not path.exists('database.sqlite3'):
        with app.app_context():
            db.create_all()

    return app