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



<<<<<<< Updated upstream
# if __name__ == '__main__':
#     app.run(port = 5555, debug = True)
=======
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


    

api.add_resource(Users, "/users")

if __name__ == '__main__':
    app.run(port = 5555, debug = True)
>>>>>>> Stashed changes

