from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

import logging
from logging.handlers import RotatingFileHandler
import os

from datetime import datetime

load_dotenv()

db_host = os.getenv("MYSQL_HOST")
db_port = os.getenv("MYSQL_PORT")
db_pwd = os.getenv("MYSQL_ROOT_PASSWORD")

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{db_pwd}@{db_host}:{db_port}/twitter_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configure logging
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

class User(db.Model):
    __tablename__ = 'USERS'

    uid = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    is_private = db.Column(db.String(300), default=False, nullable=False)
    created_on = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __init__(self, uid, username, email, is_private=False):
        self.uid = uid
        self.username = username
        self.email = email
        self.is_private = is_private

    def json(self):
        return {
            "user id": self.uid,
            "username": self.username,
            "user email": self.email,
            "is user private": self.is_private,
            "user created on": self.created_on
        }

@app.route('/users')
def get_all_users():
    users = db.session.scalars(db.select(User)).all()

    if len(users):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in users]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No users found!"
        }
    ), 404

@app.route("/user/<string:uid>")
def get_user(uid):
    user = db.session.scalars(
        db.select(User).filter_by(uid=uid).
        limit(1)
    ).first()

    if user:
        app.logger.info("User found!", user.json())
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404

@app.route("/user/<string:uid>", methods=["POST"])
def create_user(uid):
    data = request.get_json()
    errors = []
    existing_username = User.query.filter_by(username=data['username']).first()
    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_username:
        errors.append(f"Username {data['username']} already exists")
    if existing_email:
        errors.append(f"User with email address {data['email']} already exists")
    if errors:
        return jsonify({
            'code': 400,
            'message': errors
        }), 400

    user = User(uid=uid, **data)
    try:
        db.session.add(user)
        db.session.commit()
        app.logger.info("User added into database:", user.json())
    except IntegrityError as e:
        return jsonify({
            "code": 400,
            "data": {
                "uid": uid
            },
            "message": f"An error occurred creating the user. {e}"
        }), 400
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "uid": uid
            },
            "message": f"An error occurred creating the user. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": user.json()
    }), 201

@app.route("/user/<string:uid>", methods=["PUT"])
def update_user(uid):
    user = db.session.scalars(
        db.select(User).filter_by(uid=uid).
        limit(1)
    ).first()

    if not user:
        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404

    app.logger.info("User found, proceeding to update!", user.json())
    data = request.get_json()

    try:
        if data.get('username'):
            user.username = data['username']
        if data.get('email'):
            user.email = data['email']
        if data.get('is_private'):
            user.is_private = data['is_private']

        db.session.commit()
        app.logger.info("User updated in database:", user.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "uid": uid
            },
            "message": f"An error occurred when updating the user. {e}"
        }), 500

    return jsonify({
        "code": 200,
        "data": user.json()
    }), 200

@app.route('/user/<string:uid>', methods=['DELETE'])
def delete_user(uid):
    user = db.session.scalars(
        db.select(User).filter_by(uid=uid).
        limit(1)
    ).first()

    if not user:
        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404
    app.logger.info("User found, proceeding to delete!", user.json())
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "uid": uid
            },
            "message": f"An error occurred when deleting the user. {e}"
        }), 500

    return jsonify(
        {
            "code": 204,
            "message": "User deleted successfully"
        }
    ), 204

if __name__ == "__main__":
    app.logger.info("Users API is running at port 5100")
    app.run(host='0.0.0.0', port=5100, debug=True)
