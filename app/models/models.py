from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='cliente')  # 'admin', 'peluquero', 'cliente'
    created_at = db.Column(db.DateTime, default=datetime.now)

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    servicio = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # 'pendiente', 'confirmado', 'cancelado'

    cliente = db.relationship('User', backref='turnos')