from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import re
from sqlalchemy.ext.hybrid import hybrid_property
# from app import bcrypt

db = SQLAlchemy()



class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    price= db.Column(db.Integer,nullable=False)
    onstock = db.Column(db.String, nullable=False)
    rating= db.Column(db.Integer,nullable=False)

    shoppingcarts= db.relationship('ShoppingCart', backref= 'product')
    reviews= db.relationship('Review', backref= 'product')

    def __repr__(self):
        return f"Product: Description: {self.description} \n Price: {self.price} \n Stock: {self.onstock} \n Rating: {self.rating}"


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    rating= db.Column(db.Integer,nullable=False)
    created_at= db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User', backref='review')

    def __repr__(self):
        return f"Review: {self.description} \n Rating:{self.rating} \n Posted: {self.created_at}"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone= db.Column(db.Integer,nullable=False)
    password = db.Column(db.String, nullable=False)

    shopping_cart = db.relationship('ShoppingCart', back_populates='user', uselist=False)
    reviews = db.relationship('Review', back_populates='user')
    receipts = db.relationship('Receipt', back_populates='user')

    def __repr__(self):
        return f"User.... Username:{self.username} \n Email:{self.email} \n Phone number: {self.phone} \n  Password: {self.password} "

class ShoppingCart(db.Model):
    __tablename__ = 'shoppingCarts'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)

    user = db.relationship('User', back_populates='shopping_cart')


    def __repr__(self):
        return f"Shopping Cart: {self.id} "

class Receipt(db.Model):
    __tablename__="receipts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    phone= db.Column(db.Integer,nullable=False)
    shipping_details = db.Column(db.String, nullable=False)
    delivery_address = db.Column(db.String, nullable=False)
    created_at= db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User', backref='receipt')

    def __repr__(self):
        return f"Receipt: Username: {self.username} \n Phone: {self.phone} \n Shipping Details: {self.shipping_details} \n Delivery address: {self.delivery_address}"

