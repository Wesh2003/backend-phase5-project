from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship

import re
from datetime import datetime

db = SQLAlchemy()

# Many-to-many relationship between Receipts and Products
product_receipts = db.Table('product_receipts',
                      db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
                      db.Column('receipt_id', db.Integer, db.ForeignKey('receipts.id'), primary_key=True)
                      )


class Product(db.Model):
    
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # Ensure a consistent length
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))  # Use db.String for consistency
    price = db.Column(db.Integer, nullable=False)
    onstock = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    # wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlists.id"))

    shoppingcarts = relationship('ShoppingCart', backref='product')
    # reviews = relationship('Review', backref='product')
    receipts = db.relationship('Receipt', secondary=product_receipts, backref='product')
    wishlists = relationship("Wishlist", back_populates="product")

    def __repr__(self):
        return f"Product(ID: {self.id}, Name: {self.name}, Price: {self.price}, Stock: {self.onstock}, Rating: {self.rating})"

    def to_dict(self):
        return {
            'id': self.id,
            'name':self.name,
            'description': self.description,
            'category':self.category,
            'image_url':self.image_url,
            'price':self.price,
            'onstock':self.onstock,
            'rating':self.rating
            # Add more attributes if needed
        }

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
    product = relationship('Product', backref='reviews')

    def __repr__(self):
        return f"Review(ID: {self.id}, Rating: {self.rating}, Posted: {self.created_at})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "rating":self.rating,
            "description":self.description,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "created_at":self.created_at,
            "username":self.user.name,
            "product_name": self.product.name
            }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.Integer, nullable=False)  # Use string for phone numbers
    password = db.Column(db.String(128), nullable=False)  # Assume hashed password

    shopping_cart = db.relationship('ShoppingCart', back_populates='user', uselist=False)  # Assume one shopping cart per user
    receipts = relationship('Receipt', back_populates='user')
    wishlists = relationship("Wishlist", back_populates="user")

    def __repr__(self):
        return f"User(ID: {self.id}, Username: {self.username})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.product_id,
            'email': self.user_id,
            'password':self.password,
            'phone':self.phone
            # Add more attributes if needed
        }

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_carts'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Added nullable=False

    user = db.relationship('User', back_populates='shopping_cart')
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id
            # Add more attributes if needed
        }
    
class Wishlist(db.Model):
    __tablename__= "wishlists"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = relationship('User', back_populates='wishlists')
    product = relationship('Product', back_populates='wishlists')

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'product_id': self.product_id,
    #         'user_id': self.user_id
    #         # "name": self.product.name,
    #         # "description": self.product.description,
    #         # "price": self.product.price,
    #         # "quantity": self.product.quantity,
    #         # "category": self.product.category
    #         # Add more attributes if needed
    #     }

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
            # Add more attributes if needed
        }

class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)
    delivery_address= db.Column(db.String(255), nullable=False)  # Simplified for example
    city = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User', back_populates='receipts')

    
    def __repr__(self):
        return f"Receipt(ID: {self.id}, Details: {self.details}, Date: {self.created_at})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "delivery_address":self.delivery_address,
            "city":self.city,
            "user_id": self.user_id,
            "created_at":self.created_at
            }

# class Category(db.Model):
#     __tablename__ = "categories"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)  # Changed 'category' to 'name' for clarity
#     description = db.Column(db.String(255), nullable=False)

#     products = relationship('Product', backref='category')

#     def __repr__(self):
#         return f"Category(ID: {self.id}, Name: {self.name})"