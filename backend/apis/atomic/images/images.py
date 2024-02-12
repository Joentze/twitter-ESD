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

class Image(db.Model):
    __tablename__ = 'IMAGES'

    object_id = db.Column(db.String(100), primary_key=True)
    uploader_uid = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __init__(self, object_id, uploader_uid):
        self.object_id = object_id
        self.uploader_uid = uploader_uid

    def json(self):
        return {
            "object id": self.object_id,
            "uploader uid": self.uploader_uid,
            "date created": self.date_created
        }

@app.route('/images')
def getAllImages():
    images = db.session.scalars(db.select(Image)).all()

    if len(images):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "images": [image.json() for image in images]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No images found!"
        }
    ), 404

@app.route("/imageUploadedBy/<string:uploader_uid>")
def findImagesUploadedBy(uploader_uid):
    images = db.session.scalars(
        db.select(Image).filter_by(uploader_uid=uploader_uid)
    ).all()

    if images:
        app.logger.info("Images found!")
        return jsonify(
            {
                "code": 200,
                "data": [image.json() for image in images]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Image not found."
        }
    ), 404

@app.route("/image/<string:object_id>")
def findImage(object_id):
    image = db.session.scalars(
        db.select(Image).filter_by(object_id=object_id).
        limit(1)
    ).first()

    if image:
        app.logger.info("Image found!", image.json())
        return jsonify(
            {
                "code": 200,
                "data": image.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Image not found."
        }
    ), 404

@app.route("/image/<string:object_id>", methods=["POST"])
def createImage(object_id):
    image_exists = db.session.scalars(
        db.select(Image).filter_by(object_id=object_id).
        limit(1)
    ).first()
    if image_exists:
        return jsonify({
            "code": 400,
            "message": "Image already exists!"
        }), 400

    data = request.get_json()
    image = Image(object_id=object_id, **data)

    try:
        db.session.add(image)
        db.session.commit()
        app.logger.info("Image added into database:", image.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "object_id": object_id
            },
            "message": f"An error occurred creating the image. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": image.json()
    }), 201

@app.route('/image/<string:object_id>', methods=['DELETE'])
def delete_image(object_id):
    image = db.session.scalars(
        db.select(Image).filter_by(object_id=object_id).
        limit(1)
    ).first()

    if not image:
        return jsonify(
            {
                "code": 404,
                "message": "Image not found."
            }
        ), 404
    app.logger.info("Image found, proceeding to delete!", image.json())
    try:
        db.session.delete(image)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "object_id": object_id
            },
            "message": f"An error occurred when deleting the image. {e}"
        }), 500

    return jsonify(
        {
            "code": 204,
            "message": "Image deleted successfully"
        }
    ), 204

if __name__ == "__main__":
    app.logger.info("Images API is running at port 5110")
    app.run(host='0.0.0.0', port=5110, debug=True)
