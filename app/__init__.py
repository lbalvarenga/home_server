from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "auth.login"
moment = Moment(app)

from .auth import auth
from .user import user

app.register_blueprint(auth)
app.register_blueprint(user)

from app import routes