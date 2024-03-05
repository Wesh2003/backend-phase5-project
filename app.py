from flask import Flask, make_response, request, jsonify, render_template
from flask_migrate import Migrate
# from flask_restful import Api, Resource
# from werkzeug.exceptions import NotFound
# import os
# # from flask_Bcrypt import Bcrypt
# # from dotenv import load_dotenv
# # load_dotenv()


from models import db

app = Flask(
    __name__,
    )
# bcrypt= Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoppingDatabase.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api= Api(app)

# @app.route("/")
# def home():
#     return 'hello world'

# @app.route("/products" ,methods=["GET"])
# def get_products():
#     pass
#     # products = Products.query.all()
#     # products_list = []
#     # for product in products:
#     #     product_dict ={
#     #         product.name,
#     #         product.image,
#     #         product.quantity,
#     #         product.price,
            
#     #     }
#     #     products_list.append(product_dict)
#     #     response = make_response(jsonify(products_list),200)
#     # return response 
# @app.route("/products/<int:id>",methods=[ "GET"] )
# def get_shop(id):
#     pass
#     # product = Products.query.get(id)
#     # if product:
#     #     product_dict={
#     #         "id": product.id,
#     #         "username": product.username,
#     #         "shopname": product.shopname,
#     #         "address": product.address,
#     #         "contact": product.contact,

#     #     }
#     #     response = make_response(jsonify(product_dict), 200)

#     #     return response
#     # else:
#     #     response = {"error": "id not found"}
#     #     return jsonify(response), 404
    
# @app.route("/products/<int:id>" , methods=['DELETE'])
# def delete_product(id):
#     pass
#     # product = Products.query.get(id)
#     # if not product:
#     #     return jsonify({"error":"product not found"}),404
#     # else:
        
#     #    db.session.delete(product)
#     #    db.session.commit()
#     # return jsonify ({"message":"product deleted  well"}),200



# if __name__ == '__main__':
#     app.run(port = 5555, debug = True)

