from app import db
from datetime import datetime

class Sensors(db.Model):
    __tablename__= 'sensores'
    id = db.Column(db.Integer,  primary_key = True)
    voltage = db.Column(db.Integer)
    current = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.now)

# class sensor2(db.Model):
#     __tablename__= 'sensor2'
#     id = db.Column(db.Integer,  primary_key = True)
#     dato = db.Column(db.Float)
#     fecha = db.Column(db.DateTime, default = datetime.now) 

# class sensor3(db.Model):
#     __tablename__= 'sensor3'
#     id = db.Column(db.Integer,  primary_key = True)
#     dato = db.Column(db.Float)
#     fecha = db.Column(db.DateTime, default = datetime.now) 

# class sensor4(db.Model):
#     __tablename__= 'sensor4'
#     id = db.Column(db.Integer,  primary_key = True)
#     dato = db.Column(db.Float)
#     fecha = db.Column(db.DateTime, default = datetime.now)

 