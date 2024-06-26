"""microservice for content check"""
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import TypedDict
from flask import Flask, request, jsonify
from flask_cors import CORS
from requests import post


app = Flask(__name__)
CORS(app)

# Configure logging
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler(
    'app.log', maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


class ScoreType(TypedDict):
    """typings for scores"""
    SFW: str
    NSFW: str


# Configure logging
API_URL = os.environ["HUGGING_FACE_URL"]
HUGGING_FACE_TOKEN = os.environ["HUGGING_FACE_TOKEN"]
headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}


@app.route('/post/validate')
def content_check():
    """api for text content checking"""
    req_body = request.json
    app.logger.info(req_body)
    response = post(API_URL, headers=headers, json=req_body, timeout=5000)
    print("response from hugging face", response)
    try:
        data = response.json()[0]
    except KeyError:
        for _ in range(5):
            try:
                data = response.json()[0]
                break
            except KeyError:
                continue
    scores: ScoreType = {}
    for evaluations in data:
        label, score = evaluations["label"], evaluations["score"]
        scores[label] = score
    app.logger.info(scores)
    try:
        if scores["SFW"] < scores["NSFW"] and scores["NSFW"] > 0.9:
            return jsonify(
                {"code": 200, "sfw": False}
            ), 200
        else:
            return jsonify(
                {"code": 200, "sfw": True}
            ), 200
    except Exception as e:
        print(e)
        return jsonify({"code": 500, "message": "There was an error on the server"})


if __name__ == "__main__":
    app.logger.info("Transformer API is running at port 5108")
    app.run(host='0.0.0.0', port=5108, debug=True)
