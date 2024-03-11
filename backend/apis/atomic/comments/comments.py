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

class Comment(db.Model):
    __tablename__ = 'COMMENTS'

    comment_id = db.Column(db.String(36), primary_key=True)
    commenter_uid = db.Column(db.String(100), primary_key=True)
    post_id = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date_commented = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __init__(self, commenter_uid, post_id, content):
        self.comment_id = str(uuid.uuid4())
        self.commenter_uid = commenter_uid
        self.post_id = post_id
        self.content = content

    def json(self):
        return {
            "comment id": self.comment_id,
            "commenter uid": self.commenter_uid,
            "post id": self.post_id,
            "content": self.content,
            "date commented": self.date_commented,
        }

@app.route('/comments')
def get_all_comments():
    comments = db.session.scalars(db.select(Comment)).all()

    if len(comments):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "comments": [comment.json() for comment in comments]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No one is commenting each other!"
        }
    ), 404

@app.route("/userComments/<string:commenter_uid>")
def get_user_comments(commenter_uid):
    comments = db.session.scalars(
        db.select(Comment).filter_by(commenter_uid=commenter_uid)
    )

    if comments:
        app.logger.info("Users comments found!")
        return jsonify(
            {
                "code": 200,
                "data": [comment.json() for comment in comments]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Post has no comments"
        }
    ), 404

@app.route("/comment/<string:post_id>")
def get_post_comments(post_id):
    comments = db.session.scalars(
        db.select(Comment).filter_by(post_id=post_id)
    )

    if comments:
        app.logger.info("Users comments found!")
        return jsonify(
            {
                "code": 200,
                "data": [comment.json() for comment in comments]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Post has no comments"
        }
    ), 404

@app.route("/comment/<string:post_id>", methods=["POST"])
def create_comment(post_id):
    data = request.get_json()
    comment = Comment(post_id=post_id, **data)

    comment_id_exists = db.session.scalars(
        db.select(Comment).filter_by(comment_id=comment.comment_id).
        limit(1)
    ).first()

    while comment_id_exists:
        comment.comment_id = str(uuid.uuid4())
        comment_id_exists = db.session.scalars(
            db.select(Comment).filter_by(comment_id=comment.comment_id).
            limit(1)
        ).first()

    try:
        db.session.add(comment)
        db.session.commit()
        app.logger.info("Comment added into database:", comment.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "post id": post_id
            },
            "message": f"An error occurred creating the comment. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": comment.json()
    }), 201

@app.route("/comment/<string:post_id>", methods=["PUT"])
def update_comment(post_id):
    data = request.get_json()

    comment = db.session.scalars(
        db.select(Comment).filter_by(
            post_id=post_id,
            comment_id=data['comment_id']
        ). limit(1)
    ).first()

    if not comment:
        return jsonify(
            {
                "code": 404,
                "message": "Comment not found."
            }
        ), 404

    try:
        updated = False
        if data.get('content'):
            comment.content = data['content']
            updated = True
        if updated:
            comment.date_commented = datetime.utcnow()

        db.session.commit()
        app.logger.info("Comment updated into database:", comment.json())
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "post id": post_id
            },
            "message": f"An error occurred creating the comment. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": comment.json()
    }), 201

@app.route('/comment/<string:post_id>', methods=['DELETE'])
def delete_comment(post_id):
    data = request.get_json()

    comment = db.session.scalars(
        db.select(Comment).filter_by(
            post_id=post_id,
            comment_id=data['comment_id']
        ). limit(1)
    ).first()

    if not comment:
        return jsonify(
            {
                "code": 404,
                "message": "Comment not found"
            }
        ), 404
    app.logger.info("Comment found, proceeding to delete!", comment.json())
    try:
        db.session.delete(comment)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "post id": post_id
            },
            "message": f"An error occurred when deleting the comment. {e}"
        }), 500

    return jsonify(
        {
            "code": 204,
            "message": "Comment deleted successfully"
        }
    ), 204

if __name__ == "__main__":
    app.logger.info("Comments API is running at port 5102")
    app.run(host='0.0.0.0', port=5102, debug=True)
