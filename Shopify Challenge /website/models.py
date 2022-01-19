#models.py
#defines database and data stored in it
#Developer: Shavon Thadani
#19/01/'22
from . import db
from flask_login import UserMixin
from sqlalchemy import func
class Product(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(100))
    product_data = db.Column(db.String(100))
    product_stock = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    items = db.relationship('Product')
