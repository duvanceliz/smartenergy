from app import db
from datetime import datetime

class dispositivos(db.Model):
    __tablename__= 'dispositivos'
    id = db.Column(db.Integer,  primary_key = True)
    nombre = db.Column(db.String(255),nullable=False)
    status = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default = datetime.now)

