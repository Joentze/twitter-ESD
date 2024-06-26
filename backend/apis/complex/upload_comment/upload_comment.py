"""complex microservice for uploading comments"""
import os
import json
import pika
from requests import get, post
from typing import TypedDict, List
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

API_URL = os.environ["API_URL"]
try:
    RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
    RABBITMQ_PORT = int(os.environ["RABBITMQ_PORT"])
except KeyError:
    RABBITMQ_HOST = "localhost"
    RABBITMQ_PORT = 5672
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, heartbeat=3600, blocked_connection_timeout=3600))


class CommentBody(TypedDict):
    """upload body typings"""
    content: str
    commenter_uid: str


@app.route("/upload/<string:post_id>", methods=["POST"])
def upload_post(post_id: str) -> None:
    """complex microservice to upload post"""
    try:
        data: CommentBody = request.get_json()
        content, commenter_uid = data["content"], data["commenter_uid"]
        is_sfw = check_content(content)
        try:
            if is_sfw:
                create_comment(post_id, content, commenter_uid)
            else:
                email, username = get_user_email_name(commenter_uid)
                send_content_warning(email, username)
            return jsonify({"code": 201, "message": "Successfuly uploaded comment, we'll do a quick check to see if your post violated guidelines"}), 201
        except Exception as e:
            print(e)
            return jsonify({"code": 500, "message": "there was an error on the server"}), 500

    except KeyError:
        return jsonify({"code": 400, "message": "comment data not formatted correctly"}), 400


def check_content(text: str) -> bool:
    """sends api request to NLP analyser"""
    content_check_route = f"{API_URL}/post/validate"
    response = get(content_check_route, json={"inputs": [text]}, timeout=5000)
    is_sfw = response.json()["sfw"]
    return is_sfw


def send_content_warning(email: str, username: str) -> None:
    """publishes content warning message to rabbitmq"""

    channel = connection.channel()
    channel.queue_declare(queue="notification-queue", durable=True)
    message_body: str = json.dumps(
        {"message_type": "CONTENT_WARNING", "email": email, "username": username})
    channel.basic_publish(exchange="twitter-message-exchange",
                          routing_key="email.notification", body=message_body)


def get_user_email_name(uid: str) -> tuple:
    """gets user information from uid"""
    user_info_route = f"{API_URL}/user/{uid}"
    response = get(user_info_route, timeout=5000)
    data = response.json()["data"]
    return data["user email"], data["username"]


def create_comment(post_id: str, content: str, commenter_uid: str) -> object:
    """creates comment request"""
    post_route = f"{API_URL}/comment/{post_id}"
    response = post(post_route, json={
                    "content": content, "commenter_uid": commenter_uid}, timeout=5000)
    return response.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5123, debug=True)
