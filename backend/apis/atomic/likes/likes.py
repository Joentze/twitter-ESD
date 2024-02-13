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

class Like(db.Model):
    __tablename__ = 'LIKES'

    uid = db.Column(db.String(100), primary_key=True)
    post_id = db.Column(db.String(100), primary_key=True)
    date_liked = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __init__(self, uid, post_id):
        self.uid = uid
        self.post_id = post_id

    def json(self):
        return {
            "user id": self.uid,
            "post id": self.post_id,
            "date liked": self.date_liked,
        }

@app.route('/likes')
def get_all_likes():
    likes = db.session.scalars(db.select(Like)).all()

    if len(likes):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "likes": [like.json() for like in likes]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No one is likeing each other!"
        }
    ), 404

@app.route("/like/<string:post_id>")
def get_post_likes(post_id):
    like = db.session.scalars(
        db.select(Like.uid).filter_by(post_id=post_id)
    )

    if like:
        app.logger.info("Users likeed found!")
        return jsonify(
            {
                "code": 200,
                "data": list(like)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Post has no likes"
        }
    ), 404

@app.route("/like/<string:post_id>", methods=["POST"])
def create_like(post_id):
    data = request.get_json()
    like = db.session.scalars(
        db.select(Like).filter_by(post_id=post_id, uid=data['uid']).
        limit(1)
    ).first()
    if like:
        return jsonify({
            "code": 400,
            "data": {
                "post id": post_id
            },
            "message": f"Post {post_id} has already been liked by user"
        }), 400

    like = Like(post_id=post_id, **data)

    try:
        db.session.add(like)
        db.session.commit()
        app.logger.info("Like added into database:", like.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "post id": post_id
            },
            "message": f"An error occurred creating the like. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": like.json()
    }), 201

@app.route('/like/<string:post_id>', methods=['DELETE'])
def delete_like(post_id):
    data = request.get_json()

    like = db.session.scalars(
        db.select(Like).filter_by(post_id=post_id, uid=data['uid']).
        limit(1)
    ).first()

    if not like:
        return jsonify(
            {
                "code": 404,
                "message": "Post is not liked by user"
            }
        ), 404
    app.logger.info("Like found, proceeding to delete!", like.json())
    try:
        db.session.delete(like)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "post id": post_id
            },
            "message": f"An error occurred when deleting the like. {e}"
        }), 500

    return jsonify(
        {
            "code": 204,
            "message": "Like deleted successfully"
        }
    ), 204

if __name__ == "__main__":
    app.logger.info("Likes API is running at port 5103")
    app.run(host='0.0.0.0', port=5103, debug=True)
