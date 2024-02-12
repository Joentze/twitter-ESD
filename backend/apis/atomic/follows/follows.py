from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

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

class Follow(db.Model):
    __tablename__ = 'FOLLOWS'

    follower_id = db.Column(db.String(100), primary_key=True)
    followed_id = db.Column(db.String(100), primary_key=True)
    date_followed = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id

    def json(self):
        return {
            "follower id": self.follower_id,
            "followed id": self.followed_id,
            "date followed": self.date_followed,
        }

@app.route('/follows')
def getAllFollows():
    follows = db.session.scalars(db.select(Follow)).all()

    if len(follows):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "follows": [follow.json() for follow in follows]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No one is following each other!"
        }
    ), 404

@app.route("/follow/<string:uid>")
def getUserFollowing(uid):
    follow = db.session.scalars(
        db.select(Follow.followed_id).filter_by(follower_id=uid)
    )

    if follow:
        app.logger.info("Users followed found!")
        return jsonify(
            {
                "code": 200,
                "data": list(follow)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not following anyone"
        }
    ), 404

@app.route("/follow/<string:uid>", methods=["POST"])
def createFollow(uid):
    data = request.get_json()
    follow = db.session.scalars(
        db.select(Follow).filter_by(follower_id=uid, followed_id=data['followed_id']).
        limit(1)
    ).first()
    if follow:
        return jsonify({
            "code": 400,
            "data": {
                "follower id": uid
            },
            "message": "User already followed"
        }), 400

    follow = Follow(follower_id=uid, **data)

    try:
        db.session.add(follow)
        db.session.commit()
        app.logger.info("Follow added into database:", follow.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "uid": uid
            },
            "message": f"An error occurred creating the follow. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": follow.json()
    }), 201

@app.route('/follow/<string:uid>', methods=['DELETE'])
def deleteFollow(uid):
    data = request.get_json()

    follow = db.session.scalars(
        db.select(Follow).filter_by(follower_id=uid, followed_id=data['followed_id']).
        limit(1)
    ).first()

    if not follow:
        return jsonify(
            {
                "code": 404,
                "message": "Not following selected user."
            }
        ), 404
    app.logger.info("Follow found, proceeding to delete!", follow.json())
    try:
        db.session.delete(follow)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "uid": uid
            },
            "message": f"An error occurred when deleting the follow. {e}"
        }), 500

    return jsonify(
        {
            "code": 204,
            "message": "Follow deleted successfully"
        }
    ), 204

if __name__ == "__main__":
    app.logger.info("Follows API is running at port 5104")
    app.run(host='0.0.0.0', port=5104, debug=True)
