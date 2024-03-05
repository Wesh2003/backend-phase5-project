from flask import Flask, make_response, request, jsonify, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
import os
# from flask_Bcrypt import Bcrypt
# from dotenv import load_dotenv
# load_dotenv()


from models import db, Product

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

@app.route("/")
def home():
    return 'hello world'

@app.route("/products" ,methods=["GET"])
def get_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        product_dict ={
            "id": product.id,
            "description": product.description,
            "price": product.price,
            "onstock": product.onstock,
            "rating": product.rating,
            
        }
        products_list.append(product_dict)
    response = make_response(jsonify(products_list),200)
    return response 

@app.route('/favorites', methods=['POST'])
@jwt_requires()
def add_to_favorites():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    product_id = request.json.get('product_id')
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404    
    
    if Favorite.query.filter_by(user_id=user.id, product_id=product.id).first():
        return jsonify({'message': 'Product already in favorites'}), 400

    # Add product to user's favorites
    favorite = Favorite(user_id=user.id, product_id=product.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({'message': 'Product added to favorites successfully'}), 201

    
    


# @app.route("/" ,methods=["GET"])
# @app.route("/shoppingcart" ,methods=["POST"])
# @app.route("/shoppingcart" ,methods=["GET"])
# @app.route("/shoppingcart" ,methods=["DELETE"])
# @app.route("/wishlist" ,methods=["POST"])
# @app.route("/wishlist" ,methods=["DELETE"])
# @app.route("/wishlist" ,methods=["GET"])
# @app.route("/favourites" ,methods=["POST"])
# @app.route("/favourites" ,methods=["DELETE"])
# @app.route("/favourites" ,methods=["GET"])
# @app.route("/reviews" ,methods=["POST"])
# @app.route("/reviews" ,methods=["DELETE"])
# @app.route("/reviews" ,methods=["GET"])





if __name__ == '__main__':
    app.run(port = 5555, debug = True)

