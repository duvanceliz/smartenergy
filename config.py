
import os

DBURI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{database}".format(
    username = 'root',
    password = '123456',
    hostname = 'localhost',
    database = 'test'
)

class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'millavesecreta'
    #SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
    MAIL_MAX_EMAILS = None
    MQTT_BROKER_URL = 'test.mosquitto.org'
    MQTT_BROKER_PORT = 1883
    MQTT_USERNAME = ''
    MQTT_PASSWORD = ''
    MQTT_REFRESH_TIME = 0.001  # refresh time in seconds
   

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DBURI
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///prueba.db"
   