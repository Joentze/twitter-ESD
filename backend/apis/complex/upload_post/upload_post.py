"""complex microservice for uploading post"""
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


class UploadBody(TypedDict):
    """upload body typings"""
    post_content: str
    post_location: str
    post_images: List[str]


@app.route("/upload/<string:uid>", methods=["POST"])
def upload_post(uid: str) -> None:
    """complex microservice to upload post"""
    try:
        data: UploadBody = request.get_json()
        content, location, images = data["post_content"], data["post_location"], data["post_images"]
        is_sfw = check_content(content)
        print("result check:", is_sfw)
        try:
            if is_sfw:
                print("creating post...")
                create_post(uid, content, location, images)
            else:
                print("not creating post...")
                email, username = get_user_email_name(uid)
                print(email, username)
                send_content_warning(email, username)
            return jsonify({"code": 201, "message": "Successfuly uploaded post, we'll do a quick check to see if your post violated guidelines"}), 201
        except Exception as e:
            print(e)
            return jsonify({"code": 500, "message": "there was an error on the server"}), 500

    except KeyError:
        return jsonify({"code": 400, "message": "Post data not formatted correctly"}), 400


def check_content(text: str) -> bool:
    """sends api request to NLP analyser"""
    content_check_route = f"{API_URL}/post/validate"
    response = get(content_check_route, json={"inputs": [text]}, timeout=5000)
    print(response.json())
    is_sfw = response.json()["sfw"]
    return is_sfw


def send_content_warning(email: str, username: str) -> None:
    """publishes content warning message to rabbitmq"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, heartbeat=3600, blocked_connection_timeout=3600))
    channel = connection.channel()
    channel.queue_declare(queue="notification-queue", durable=True)
    message_body: str = json.dumps(
        {"message_type": "CONTENT_WARNING", "email": email, "username": username})
    channel.basic_publish(exchange="twitter-message-exchange",
                          routing_key="email.notification", body=message_body)
    connection.close()


def get_user_email_name(uid: str) -> tuple:
    """gets user information from uid"""
    user_info_route = f"{API_URL}/user/{uid}"
    print(user_info_route)
    response = get(user_info_route, timeout=5000)
    print(response)
    data = response.json()["data"]
    return data["user email"], data["username"]


def create_post(uid: str, post_content: str, post_location: str, post_images: List[str]) -> object:
    """creates post request"""
    post_route = f"{API_URL}/post/{uid}"
    response = post(post_route, json={"post_content": post_content,
                                      "post_location": post_location, "post_images": post_images}, timeout=5000)
    return response.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5122, debug=True)
