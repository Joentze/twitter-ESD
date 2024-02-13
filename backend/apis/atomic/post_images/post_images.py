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

class PostImage(db.Model):
    __tablename__ = 'POST_IMAGE'

    object_id = db.Column(db.String(100), primary_key=True)
    post_id = db.Column(db.String(100), nullable=False)
    date_used = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __init__(self, object_id, post_id):
        self.object_id = object_id
        self.post_id = post_id

    def json(self):
        return {
            "object id": self.object_id,
            "post id": self.post_id,
            "date used": self.date_used
        }

@app.route('/postImages')
def get_all_post_post_images():
    postImage = db.session.scalars(db.select(PostImage)).all()

    if len(postImage):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "postImage": [postImage.json() for postImage in postImage]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No postImage found!"
        }
    ), 404

@app.route("/postImage/<string:post_id>")
def find_images_by_post(post_id):
    postImages = db.session.scalars(
        db.select(PostImage).filter_by(post_id=post_id)
    ).all()

    if postImages:
        app.logger.info("PostImage found!")
        return jsonify(
            {
                "code": 200,
                "data": [postImage.json() for postImage in postImages]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "PostImage not found."
        }
    ), 404

@app.route("/postImage/<string:object_id>", methods=["POST"])
def create_post_image(object_id):
    data = request.get_json()

    image_exists = db.session.scalars(
        db.select(PostImage).filter_by(object_id=object_id, post_id=data['post_id']).
        limit(1)
    ).first()
    if image_exists:
        return jsonify({
            "code": 400,
            "message": "PostImage already exists!"
        }), 400

    postImage = PostImage(object_id=object_id, **data)

    try:
        db.session.add(postImage)
        db.session.commit()
        app.logger.info("PostImage added into database:", postImage.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "object_id": object_id
            },
            "message": f"An error occurred creating the postImage. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": postImage.json()
    }), 201

@app.route('/postImage/<string:object_id>', methods=['DELETE'])
def delete_image(object_id):
    data = request.get_json()

    postImage = db.session.scalars(
        db.select(PostImage).filter_by(object_id=object_id, post_id=data['post_id']).
        limit(1)
    ).first()

    if not postImage:
        return jsonify(
            {
                "code": 404,
                "message": "PostImage not found."
            }
        ), 404
    app.logger.info("PostImage found, proceeding to delete!", postImage.json())
    try:
        db.session.delete(postImage)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "object_id": object_id
            },
            "message": f"An error occurred when deleting the postImage. {e}"
        }), 500

    return jsonify(
        {
            "code": 204,
            "message": "PostImage deleted successfully"
        }
    ), 204

if __name__ == "__main__":
    app.logger.info("PostPostImages API is running at port 5111")
    app.run(host='0.0.0.0', port=5111, debug=True)
