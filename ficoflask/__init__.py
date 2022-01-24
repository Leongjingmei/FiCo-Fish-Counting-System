from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']="1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ficopostgres:123456@localhost:5432/ficodatabase2'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from ficoflask import routes
