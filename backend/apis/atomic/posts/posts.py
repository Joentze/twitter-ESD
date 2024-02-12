from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

import logging
from logging.handlers import RotatingFileHandler
import os

import uuid
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

class Post(db.Model):
    __tablename__ = 'POSTS'

    post_id = db.Column(db.String(36), primary_key=True)
    poster_uid = db.Column(db.String(100), nullable=False)
    post_content = db.Column(db.String(300))
    post_location = db.Column(db.String(300))
    date_posted = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __init__(self, poster_uid, post_content, post_location):
        self.post_id = str(uuid.uuid4())
        self.poster_uid = poster_uid
        self.post_content = post_content
        self.post_location = post_location

    def json(self):
        return {
            "post id": self.post_id,
            "poster id": self.poster_uid,
            "post content": self.post_content,
            "post location": self.post_location,
            "date posted": self.date_posted
        }

@app.route('/posts')
def getAllPosts():
    posts = db.session.scalars(db.select(Post)).all()

    if len(posts):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "posts": [post.json() for post in posts]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No posts found!"
        }
    ), 404

@app.route("/post/<string:post_id>")
def getPost(post_id):
    post = db.session.scalars(
        db.select(Post).filter_by(post_id=post_id).
        limit(1)
    ).first()

    if post:
        app.logger.info("Post found!", post.json())
        return jsonify(
            {
                "code": 200,
                "data": post.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Post not found."
        }
    ), 404

@app.route("/post/<string:poster_uid>", methods=["POST"])
def createPost(poster_uid):
    data = request.get_json()
    post = Post(poster_uid=poster_uid, **data)

    post_id_exists = db.session.scalars(
        db.select(Post).filter_by(post_id=post.post_id).
        limit(1)
    ).first()

    while post_id_exists:
        post.post_id = str(uuid.uuid4())
        post_id_exists = db.session.scalars(
            db.select(Post).filter_by(post_id=post.post_id).
            limit(1)
        ).first()

    try:
        db.session.add(post)
        db.session.commit()
        app.logger.info("Post added into database:", post.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "poster_uid": poster_uid
            },
            "message": f"An error occurred creating the post. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": post.json()
    }), 201

@app.route("/post/<string:post_id>", methods=["PUT"])
def updatePost(post_id):
    post = db.session.scalars(
        db.select(Post).filter_by(post_id=post_id).
        limit(1)
    ).first()

    if not post:
        return jsonify(
            {
                "code": 404,
                "message": "Post not found."
            }
        ), 404

    app.logger.info("Post found, proceeding to update!", post.json())
    data = request.get_json()

    try:
        if data.get('post_content'):
            post.post_content = data['post_content']
        if data.get('post_location'):
            post.post_location = data['post_location']

        db.session.commit()
        app.logger.info("Post updated in database:", post.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "post_id": post_id
            },
            "message": f"An error occurred when updating the post. {e}"
        }), 500

    return jsonify({
        "code": 200,
        "data": post.json()
    }), 200

@app.route('/post/<string:post_id>', methods=['DELETE'])
def deletePost(post_id):
    post = db.session.scalars(
        db.select(Post).filter_by(post_id=post_id).
        limit(1)
    ).first()

    if not post:
        return jsonify(
            {
                "code": 404,
                "message": "Post not found."
            }
        ), 404
    app.logger.info("Post found, proceeding to delete!", post.json())
    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "post_id": post_id
            },
            "message": f"An error occurred when deleting the post. {e}"
        }), 500

    return jsonify(
        {
            "code": 204,
            "message": "Post deleted successfully"
        }
    ), 204

if __name__ == "__main__":
    app.logger.info("Posts API is running at port 5101")
    app.run(host='0.0.0.0', port=5101, debug=True)
