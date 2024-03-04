from flask import Flask, make_response, request, jsonify, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
import os
# from flask_Bcrypt import Bcrypt
# from dotenv import load_dotenv
# load_dotenv()


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

@app.route("/")
def home():
    return 'hello world'


if __name__ == '__main__':
    app.run(port = 5555, debug = True)

