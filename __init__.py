from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import email_validator
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'arandomstring'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://admin3:@GitPa$$w0rd#@54.74.234.11/finalproject_group3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'ctrl.alt.elite.2021@gmail.com'
app.config['MAIL_PASSWORD'] = '08042021'

mail = Mail(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes, errors
