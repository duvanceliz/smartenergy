from app import db
from flask_login import UserMixin
from datetime import datetime

class usuarios(UserMixin,db.Model):
    __tablename__='usuarios'
    id = db.Column(db.Integer,  primary_key = True)
    nombre = db.Column(db.String(50), unique= True,nullable=False)
    contraseña = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)
    fecha = db.Column(db.DateTime, default = datetime.now)
    def __repr__(self):
        return self.nombre