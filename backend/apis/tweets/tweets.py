from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

import logging
from logging.handlers import RotatingFileHandler
import os

import uuid

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

class Tweet(db.Model):
    __tablename__ = 'tweets'

    tweet_id = db.Column(db.CHAR(36), primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, content):
        self.tweet_id = str(uuid.uuid4())
        self.user_id = user_id
        self.content = content

    def json(self):
        return {
            "tweet id: ": self.tweet_id,
            "user id: ": self.user_id,
            "content: ": self.content,
            "created at: ": self.created_at
        }

@app.route('/')
def welcome():
    return "Welcome to the realm of tweets!"

@app.route('/test')
def testConnection():
    try:
        # Query the database (replace this with your actual query)
        tweet = db.session.scalars(db.select(Tweet)).first()
        if tweet:
            return f"Connected to the database. {tweet.json()}"
        else:
            return "No user found in the database."

    except Exception as e:
        return f"Error connecting to the database: {str(e)}"

@app.route('/tweets')
def getAllTweetes():
    tweets = db.session.scalars(db.select(Tweet)).all()

    if len(tweets):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tweets": [tweet.json() for tweet in tweets]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No birds chirping!"
        }
    ), 404

@app.route("/tweet/<string:tweet_id>")
def findTweet(tweet_id):
    tweet = db.session.scalars(
        db.select(Tweet).filter_by(tweet_id=tweet_id).
        limit(1)
    ).first()

    if tweet:
        return jsonify(
            {
                "code": 200,
                "data": tweet.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Tweet not found."
        }
    ), 404

@app.route("/tweet/<string:user_id>", methods=["POST"])
def createTweet(user_id):
    data = request.get_json()
    tweet = Tweet(user_id=user_id, **data)

    tweet_id_exists = db.session.scalars(
        db.select(Tweet).filter_by(tweet_id=tweet.tweet_id).
        limit(1)
    ).first()

    while tweet_id_exists:
        tweet.tweet_id = str(uuid.uuid4())
        tweet_id_exists = db.session.scalars(
            db.select(Tweet).filter_by(tweet_id=tweet.tweet_id).
            limit(1)
        ).first()

    try:
        app.logger.info(tweet.json())
        db.session.add(tweet)
        app.logger.info("added")
        db.session.commit()
        app.logger.info("After commit")
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": {
                "user_id": user_id
            },
            "message": f"An error occurred creating the tweet. {e}"
        }), 500

    return jsonify({
        "code": 201,
        "data": tweet.json()
    }), 201

if __name__ == "__main__":
    print("This is running!")
    app.run(host='0.0.0.0', port=5100, debug=True)
