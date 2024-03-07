from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import re
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # Ensure a consistent length
    description = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))  # Use db.String for consistency
    price = db.Column(db.Integer, nullable=False)
    onstock = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    shoppingcarts = relationship('ShoppingCart', backref='product')
    reviews = relationship('Review', backref='product')

    def __repr__(self):
        return f"Product(ID: {self.id}, Name: {self.name}, Price: {self.price}, Stock: {self.onstock}, Rating: {self.rating})"

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Define the relationship with User more clearly for multiple reviews
    user = relationship('User', backref='reviews')

    def __repr__(self):
        return f"Review(ID: {self.id}, Rating: {self.rating}, Posted: {self.created_at})"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False)  # Use string for phone numbers
    password = db.Column(db.String(128), nullable=False)  # Assume hashed password

    shopping_cart = relationship('ShoppingCart', back_populates='user', uselist=False)  # Assume one shopping cart per user
    receipts = relationship('Receipt', back_populates='user')

    def __repr__(self):
        return f"User(ID: {self.id}, Username: {self.username})"

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_carts'  # Use snake_case for table names

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = relationship('User', back_populates='shopping_cart')

    def __repr__(self):
        return f"ShoppingCart(ID: {self.id})"
    
class Wishlist(db.Model):
    __tablename__= "wishlists"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = relationship('User', back_populates='shopping_cart')
    wishlists = relationship('wishlist', back_populates='user', uselist=False)  

    

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(255), nullable=False)  # Simplified for example
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship('User', back_populates='receipts')

    def __repr__(self):
        return f"Receipt(ID: {self.id}, Details: {self.details}, Date: {self.created_at})"

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # Changed 'category' to 'name' for clarity
    description = db.Column(db.String(255), nullable=False)

    products = relationship('Product', backref='category')

    def __repr__(self):
        return f"Category(ID: {self.id}, Name: {self.name})"
