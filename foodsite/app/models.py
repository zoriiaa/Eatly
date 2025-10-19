from sqlalchemy import Enum
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    gender = db.Column(Enum('Чоловік', 'Жінка', name='gender_variants'), nullable=True)
    goal = db.Column(Enum('Набрати вагу', 'Скинути вагу', 'Підтримувати вагу', name='goal_types'), nullable=True)
    goal_weight = db.Column(db.Float)