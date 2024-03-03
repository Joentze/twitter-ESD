from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from transformers import pipeline

import requests
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
API_URL = "https://api-inference.huggingface.co/models/michellejieli/NSFW_text_classifier"
headers = {"Authorization": "Bearer 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"}
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)



@app.route('/posts/validate')
def content_check(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    
    data=response.json()[0]
    sfw = data[0]
    nsfw = data[1]
    
    if sfw['score']>nsfw['score']:
        return True
    else:
        return False


	
# output = content_check({
# 	"inputs": "I like you. I love you",
# })

# print(output)
