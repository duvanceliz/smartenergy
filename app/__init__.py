from distutils.command.config import config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt 
from flask_mail import Mail
from itsdangerous import TimedJSONWebSignatureSerializer


app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

# UPLOAD_FOLDER = os.path.abspath('./static/')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


login_manager = LoginManager(app)
login_manager.login_view = 'iniciarsesion'
db = SQLAlchemy(app)
mqtt = Mqtt(app)
mail = Mail(app)
s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'],expires_in=900)

from app.routes import *
from app.mqtt import *