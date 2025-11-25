import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'temporary_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'
