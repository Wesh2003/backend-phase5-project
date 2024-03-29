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

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)



app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
# app.config['JWT_SECRET_KEY'] = 'aec889f7f5b11e6ca2de8739ad202d5d4ce716cf377cc07d'

jwt = JWTManager(app)

migrate = Migrate(app, db)

db.init_app(app)
api= Api(app)


@app.route("/")
def home():
    return 'Shop Mate'

class Users(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity
        user = User.query.filter_by(id=current_user_id).first()
        if user:
            response = {'id': user.id, 'phone': user.phone, 'name': user.name ,'email': user.email} 
            return make_response(jsonify(response), 200)
        else:
            return {"error":"user not found"}, 
    def post(self):    
        email = request.json.get('email')
        password = request.json.get('password')

        if email and password:
            # Query the database using the email
            user = User.query.filter_by(email=email).first()
            

            if user and password:
                # Assuming user.id is the user ID
                access_token = create_access_token(identity=user.email)
                return {'access_token': access_token , 'id': user.id}, 200
            else:
                return {'message': "Invalid credentials"}, 401
        else:
            return {'message': "Invalid credentials"}, 401
# app.route('/login', methods=['GET'])
# def post(self):
#         data = request.get_json()
#         name = data.get('username')
#         password = data.get('password')       
#         user = User.query.filter_by(name).first()
#         if user and password:
#                 access_token = create_access_token(identity=user.name)
#                 return {'access_token': access_token , 'id': user.id}, 200
#         else:
#                 return {"message": "invalid credentials"}, 401


@app.route("/users", methods=["GET"])
def get_users():
    try:
        # Retrieve all users from the database
        users = User.query.all()
        
        # Serialize the users data into a list of dictionaries
        users_data = [{
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone
            # Add more fields as needed
        } for user in users]

        # Return the list of users as JSON response
        return jsonify(users_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
                "id": user.id,
                "name": user.name,
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
        # Handle any exceptions that occur during processing
        print(e)  # Print the exception for debugging purposes
        response = {"error": "An error occurred"}
        return jsonify(response), 500
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

   
    name = data.get('name')
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
    # Retrieve user_id from the request JSON

    user_id = request.json.get('userId') or request.json.get('user_id')


    # Check if the user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    product_id = request.json.get('product_id')
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    existing_wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_wishlist_item:
        return jsonify({'message': 'Product already in wishlist'}), 400

    wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()

    return jsonify({'message': 'Product added to wishlist successfully'}), 201
@app.route('/wishlists/remove/<int:product_id>', methods=['DELETE'])
def remove_from_wishlist(product_id):
    # Retrieve the user ID from the request JSON
    user_id = request.json.get('user_id')

    # Check if the user ID is provided
    if not user_id:
        return jsonify({'message': 'User ID not provided'}), 400

    # Check if the product exists in the wishlist
    wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not wishlist_item:
        return jsonify({'message': 'Product not found in wishlist'}), 404

    # Delete the wishlist item from the database
    db.session.delete(wishlist_item)
    db.session.commit()

    return jsonify({'message': 'Product removed from wishlist successfully'}), 200

@app.route('/wishlists/<int:user_id>', methods=['GET'])
def get_wishlist_products(user_id):
    # Retrieve the user from the database based on the user ID
    user = User.query.get(user_id)

    # Check if the user exists
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Retrieve the wishlist items for the specified user
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
    all_reviews = Review.query.all()
    review_dict= [review.to_dict() for review in all_reviews]
    response= make_response(jsonify(review_dict), 200)
    return response

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
    
    try:
        new_review= Review(description = description, rating= rating, product_id = product_id, user_id= user_id)
        db.session.add(new_review)
        db.session.commit()

        new_review_dict= new_review.to_dict()
        response = make_response(jsonify(new_review_dict), 200)
        return response
    except Exception as e:
        response= make_response({'error': str(e)}, 400)
        return response
    # if not all([description, rating, product_id, user_id]):
    #     return jsonify({"error": "Missing fields!"}), 400

    # Create a new review object
    # new_review = Review(
    #     description=description,
    #     rating=rating,
    #     product_id=product_id,
    #     user_id=user_id
    # )

    # db.session.add(new_review)
    # db.session.commit()

    # review_details = {
    #     "id": new_review.id,
    #     "description": new_review.description,
    #     "rating": new_review.rating,
    #     "created_at": new_review.created_at.isoformat(),
    #     "product_id": new_review.product_id,
    #     "user_id": new_review.user_id
    # }

    # ans = make_response(jsonify(review_details),200)
    # return ans
        
       
         

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

class Cart(Resource):
    def post(self):
        try:
            data = request.get_json()
            product_id = data.get('product_id')
            user_id = data.get('user_id')

            # Validate input data
            if not product_id or not user_id:
                raise ValueError("Both 'product_id' and 'user_id' are required.")
            
            

            # Create new Cart object
            new_cart_item = ShoppingCart(product_id=product_id, user_id=user_id)
            product = Product.query.filter_by(id=product_id).first()
            
            # Add new item to the database
            new_shopping_cart_item = ShoppingCart(product_id=new_cart_item.product_id, user_id=new_cart_item.user_id)
            db.session.add(new_shopping_cart_item)
            db.session.commit()

            # Prepare response
            new_cart_item_dict = {
                "product_id": new_cart_item.product_id,
                "user_id": new_cart_item.user_id,
                "product":{
                        'name': product.name,
                        'description': product.description,
                        'category': product.category,
                        'image_url': product.image_url,
                        'price': product.price,
                        'onstock': product.onstock,
                        'rating': product.rating

                }
            }
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

    def get(self):
        try:
            all_shopping_cart_items = ShoppingCart.query.all()
            shopping_cart_items_dict = [item.to_dict() for item in all_shopping_cart_items]
            
            # Include product details in the response
            shopping_cart_items_with_products = []
            for item in shopping_cart_items_dict:
                product = Product.query.get(item['product_id'])
                if product:
                    item['product'] = {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'category': product.category,
                        'image_url': product.image_url,
                        'price': product.price,
                        'onstock': product.onstock,
                        'rating': product.rating
                    }
                shopping_cart_items_with_products.append(item)
            
            return jsonify(shopping_cart_items_with_products), 200
        
        except Exception as e:
            return make_response({'error': str(e)}, 500)
    def delete(self, id):
        try:
            item = ShoppingCart.query.filter_by(id=id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
                return make_response("Item deleted", 200)
            else:
                return make_response("Item not found", 404)
        
        except Exception as e:
            return make_response({'error': str(e)}, 500)
        

@app.route('/shoppingcart/<int:id>', methods=['GET'])
def get_shopping_products(id):
    # Retrieve the shopping cart items for the specified user
    cart = ShoppingCart.query.filter_by(user_id=id).all()

    cart_data = []
    for item in cart:
        product = Product.query.get(item.product_id)
        if product:
            cart_data.append({
                'product_id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image_url': product.image_url
            })

    return jsonify({'cart': cart_data}), 200

@app.route('/shoppingcarts/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ShoppingCart.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify(message='Product deleted successfully'), 200
    else:
        return jsonify(message='Product not found'), 404




        
  
@app.route("/receipt/last", methods=["GET"])
def get_last_receipt():
    last_receipt = Receipt.query.order_by(min(Receipt.id)).first()

    if last_receipt:
        return jsonify(last_receipt.to_dict()), 200
    else:
        return jsonify({"message": "No receipts found"}), 404

@app.route("/receipt", methods=["GET"])
def get_all_receipts():
    all_receipts = Receipt.query.all()
    receipt_dict= [receipt.to_dict() for receipt in all_receipts]
    response= make_response(jsonify(receipt_dict), 200)
    return response

@app.route('/receipt', methods=['POST'])
def add_receipt():
    data = request.json
    
    # Extract receipt details from the request JSON
    delivery_address = data.get('delivery_address')
    city = data.get('city')
    user_id = data.get('user_id')

    try:
        new_receipt= Receipt(delivery_address=delivery_address, city=city, user_id=user_id)
        db.session.add(new_receipt)
        db.session.commit()

        new_receipt_dict= new_receipt.to_dict()
        response = make_response(jsonify(new_receipt_dict), 200)
        return response
    except Exception as e:
        response= make_response({'error': str(e)}, 400)
        return response
    
    except Exception as e:
        # Return an error response if something goes wrong
        return jsonify({'error': str(e)}), 400

@app.route('/receipt/<int:receipt_id>', methods=['DELETE'])
def delete_receipt(receipt_id):
    receipt = Receipt.query.get(receipt_id)
    if receipt:
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(message='Receipt deleted successfully'), 200
    else:
        return jsonify(message='Receipt not found'), 404


    

api.add_resource(Users, "/users")
api.add_resource(Cart, "/shoppingcart")

if __name__ == '__main__':
    app.run(port = 5555, debug = True)


