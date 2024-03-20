from flask import Flask, make_response, request, jsonify, render_template, session
from flask_migrate import Migrate

from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from models import db, User, ShoppingCart, Receipt, Wishlist
from auth import Auth
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
# from flask_Bcrypt import Bcrypt
# from dotenv import load_dotenv
# load_dotenv()



from models import db, Product,Review,ShoppingCart

app = Flask(
    __name__,
    )
# bcrypt= Bcrypt(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoppingDatabase.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/*": {"origins": "*"}})



app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

migrate = Migrate(app, db)

db.init_app(app)
api= Api(app)


@app.route("/")
def home():
    return 'Shop Mate'

class Users(Resource):
    def get(self):
        users = User.query.all()
        response = [{'id': user.id, 'phone': user.phone, 'name': user.name ,'email': user.email} for user in users]
        return make_response(jsonify(response))
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')

        if email and password:
            # Query the database using the email
            user = User.query.filter_by(email=email).first()

            if user and password:
                # Assuming user.id is the user ID
                access_token = create_access_token(identity=user.email)
                return {'user_id': user.id, 'access_token': access_token}, 200
            else:
                return {'message': "Invalid credentials"}, 401
        else:
            return {'message': "Invalid credentials"}, 401

@app.route('/users/<string:name>', methods=['GET'])
def user_by_name(name):
    user = User.query.filter_by(name=name).first()
    try:
        if user:
            response = {
                "name": user.name,
                "id": user.id,
                "email": user.email,
                "phone": user.phone
            }
            return jsonify(response), 200
        else:
            response = {"error": "No such user"}
            return jsonify(response), 404
    except Exception as e:
        response = {"error": str(e)}
        return jsonify(response), 500
@app.route('/users/<int:id>', methods=['GET'])
def user_by_id(id):
    try:
        # Attempt to retrieve the user by ID from the database
        user = User.query.get(id)
        
        # Check if the user exists
        if user:
            # User found, create the response
            response = {
                "name": user.name,
                "id": user.id,
                "email": user.email,
                "phone": user.phone
            }
            # Return the response with status code 200 (OK)
            return jsonify(response), 200
        else:
            # User not found, create the error response
            response = {"error": "No such user"}
            # Return the error response with status code 404 (Not Found)
            return jsonify(response), 404
    except Exception as e:
        # An unexpected error occurred, create the error response
        response = {"error": str(e)}
        # Return the error response with status code 500 (Internal Server Error)
        return jsonify(response), 500

    
@app.route("/products/<int:id>", methods=["PATCH"])
def update_product_category(id):
    product = Product.query.get(id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    new_category = data.get("category")

    if not new_category:
        return jsonify({"message": "Category not provided"}), 400

    product.category = new_category
    db.session.commit()

    return jsonify({"message": "Product category updated successfully"}), 200
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

   
    name = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    

    if not name or not email or not password or not phone:
        return jsonify({"error": "Incomplete or incorrect data provided"}), 400

    user = User.query.filter_by(name=name).first()  
    if not user:
        user = User(name=name, email=email, password=password, phone=phone)
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
            "name":product.name,
            "description": product.description,
            "price": product.price,
            "onstock": product.onstock,
            "rating": product.rating,
            "image_url":product.image_url,
            "category":product.category
            
        }
        
        products_list.append(product_dict)
    response = make_response(jsonify(products_list),200)
    return response

@app.route('/wishlists/add', methods=['POST'])
def add_to_wishlists():

    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']

    product_id = request.json.get('product_id')
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    existing_wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_wishlist_item:
        return jsonify({'message': 'Product already in wishlist'}), 400

    wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()

    return jsonify({'message': 'Product added to wishlist successfully'}), 201


@app.route('/wishlists/remove', methods=['DELETE'])
def remove_from_wishlists():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']

    
    product_id = request.json.get('product_id')

    wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not wishlist_item:
        return jsonify({'error': 'Product not found in wishlist'}), 404

    db.session.delete(wishlist_item)
    db.session.commit()

    return jsonify({'message': 'Product removed from wishlist successfully'}), 200
    

@app.route('/wishlists/<int:id>', methods=['GET'])
def get_wishlist_products():

    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    
    
    
    
    user_wishlist = Wishlist.query.filter_by(user_id=user_id).all()


    wishlist_data = []
    for item in user_wishlist:
        product = Product.query.get(item.product_id)
        wishlist_data.append({
            'product_id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image_url': product.image_url
        })

    return jsonify({'wishlist': wishlist_data}), 200

    

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

@app.route('/products', methods=["PATCH"])

def patch_products():
    data = request.json

    onstock = data.get('onstock')
    id = data.get('id')
    product = Product.query.get(id)

    if product:
        product.onstock = onstock

        db.session.commit()
        return jsonify("stock updated"),200
    else:
        return jsonify("error updating stock"), 400



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

@app.route("/shoppingcart", methods=["POST"])
def add_to_cart():
    try:
        data = request.get_json()

        # Validate input data
        if 'product_id' not in data or 'user_id' not in data:
            raise ValueError("Both 'product_id' and 'user_id' are required.")
        
        product_id = data['product_id']
        user_id = data['user_id']

        # Create new ShoppingCart object
        new_cart_item = ShoppingCart(product_id=product_id, user_id=user_id)
        
        # Add new item to the database
        db.session.add(new_cart_item)
        db.session.commit()

        # Prepare response
        new_cart_item_dict = new_cart_item.to_dict()
        response = jsonify(new_cart_item_dict)
        response.status_code = 200
        return response 
    
    except KeyError as e:
        error_message = f"Missing key: {e}"
        return make_response({'error': error_message}, 400)
    
    except ValueError as e:
        return make_response({'error': str(e)}, 400)
    
    except Exception as e:
        return make_response({'error': str(e)}, 500)

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
  
@app.route("/receipt", methods = ["GET" ])



@app.route('/receipt', methods=['POST'])
def add_receipt():
    data = request.json
    
    # Extract receipt details from the request JSON
    details = data.get('details')
    user_id = data.get('user_id')

    if not details or not user_id:
        return jsonify({'error': 'Both details and user_id are required.'}), 400
    
    created_at = datetime.now()

    try:
        # Create a new Receipt object
        new_receipt = Receipt(details=details, created_at=created_at, user_id=user_id)
        
        # Add the new receipt to the database
        db.session.add(new_receipt)
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Receipt added successfully'}), 201
    
    except Exception as e:
        # Return an error response if something goes wrong
        return jsonify({'error': str(e)}), 400


    

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


