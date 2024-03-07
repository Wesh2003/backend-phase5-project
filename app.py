from flask import Flask, make_response, request, jsonify, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from models import db, User, ShoppingCart, Receipt, Category, Wishlist
from auth import Auth
import os
# from flask_Bcrypt import Bcrypt
# from dotenv import load_dotenv
# load_dotenv()


from models import db, Product,Review,ShoppingCart

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

class Users(Resource):
    def get(self):
        users = User.query.all()
        response = [{'id': user.id, 'name': user.name ,'email': user.email} for user in users]
        return make_response(jsonify(response))

@app.route('/users/<int:id>', methods=['GET'])
def user_by_id(id):
    user = User.query.get(id)
    try:
        if user:
            response = [{
            "name": user.name, "id": user.id, "email": user.email
            }]
        return jsonify(response), 200
    except:
            response = {"error": "No such user"}
            return jsonify(response), 404
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

   
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Incomplete or incorrect data provided"}), 400

    user = User.query.filter_by(name=name).first()  
    if not user:
        user = User(name=name, email=email)
        Auth.set_password(user, password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"message": "User already registered"}), 400

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


@app.route('/favourites', methods=['POST'])
@jwt_required()
def add_to_favourites():


    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    product_id = request.json.get('product_id')
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404    
    
    if Favourite.query.filter_by(user_id=user.id, product_id=product.id).first():
        return jsonify({'message': 'Product already in favourites'}), 400

    # Add product to user's favorites
    favourite = Favourite(user_id=user.id, product_id=product.id)
    db.session.add(favourite)
    db.session.commit()

    return jsonify({'message': 'Product added to favourites successfully'}), 201


@app.route('/favourites/remove', methods=['DELETE'])
@jwt_required()
def remove_from_favourites():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    product_id = request.json.get('product_id')
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    favourite = Favourite.query.filter_by(user_id=user.id, product_id=product.id).first()
    if not favourite:
        return jsonify({'message': 'Product not in favourites'}), 400

    # Remove product from user's favourites
    db.session.delete(favourite)
    db.session.commit()

    return jsonify({'message': 'Product removed from favourites successfully'}), 200

@app.route('/favourites', methods=['GET'])
@jwt_required()
def get_favourite_products():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    favourites = Favourite.query.filter_by(user_id=user.id).all()
    favourite_products = [{'id': fav.product_id, 'name': fav.product.name} for fav in favourites]

    return jsonify({'favourites': favourite_products}), 200
    
    


# @app.route("/" ,methods=["GET"])
# 
# @app.route("/shoppingcart" ,methods=["POST"])
# @app.route("/shoppingcart" ,methods=["GET"])
# @app.route("/shoppingcart" ,methods=["DELETE"])
# @app.route("/wishlist" ,methods=["POST"])
# @app.route("/wishlist" ,methods=["DELETE"])
# @app.route("/wishlist" ,methods=["GET"])

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_list = []
    for review in reviews:
        review_dic={
            'id': review.id,
            'description': review.description,
            'rating': review.rating,
            'created_at': review.created_at,
            'product_id': review.product_id,
            'user_id': review.user_id
        }
        review_list.append(review_dic)
    ans = make_response(jsonify(review_list),200)
    return ans

@app.route("/reviews", methods=["POST"])
def create_review():
    data = request.json
    description = data.get("description")
    rating = data.get("rating")
    product_id = data.get("product_id")
    user_id = data.get("user_id")
    
    if not all([description, rating, product_id, user_id]):
        return jsonify({"error": "Missing fields!"}), 400

    # Create a new review object
    new_review = Review(
        description=description,
        rating=rating,
        product_id=product_id,
        user_id=user_id
    )

    db.session.add(new_review)
    db.session.commit()

    review_details = {
        "id": new_review.id,
        "description": new_review.description,
        "rating": new_review.rating,
        "created_at": new_review.created_at.isoformat(),
        "product_id": new_review.product_id,
        "user_id": new_review.user_id
    }

    ans = make_response(jsonify(review_details),200)
    return ans
        
       
         

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify(message='Review deleted successfully'), 200
    else:
        return jsonify(message='Review not found'), 404


@app.route("/reviews/<int:review_id>", methods=["PATCH"])
def update_review(review_id):
    data = request.json
    description = data.get("description")
    rating = data.get("rating")

    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    if description:
        review.description = description
    if rating:
        review.rating = rating

    db.session.commit()

    review_details = {
        "id": review.id,
        "description": review.description,
        "rating": review.rating,
        "created_at": review.created_at.isoformat(),
        "product_id": review.product_id,
        "user_id": review.user_id
    }
    ans = make_response(jsonify(review_details))
    return ans



@app.route("/shoppingcart" ,methods=["POST"])
def  add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = data.get('user_id')

    try:
        new_cart_item = ShoppingCart(product_id = product_id, user_id = user_id)
        db.session.add(new_cart_item)
        db.session.commit()

        new_cart_item_dict = new_cart_item.to_dict()
        response = make_response(jsonify(new_cart_item_dict), 200)
        return response 
    
    except Exception as e:
        response = make_response({'error': str(e)}, 400)
        return response
    
@app.route("/shoppingcart" ,methods=["GET"])
def display_products_in_cart():
    all_shopping_cart_items = ShoppingCart.query.all()
    shopping_cart_items_dict = [item.to_dict() for item in all_shopping_cart_items]
    response = make_response(jsonify(shopping_cart_items_dict), 200)
    return response 

@app.route("/shoppingcart/<int:id>" ,methods=["DELETE"])
def delete_shopping_cart_item(id):
    item = ShoppingCart.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    response =  make_response("Item deleted", 200)
    return response  



    

api.add_resource(Users, "/users")

if __name__ == '__main__':
    app.run(port = 5555, debug = True)

