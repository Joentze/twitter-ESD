"""complex microservice for uploading post"""
from requests import get
from typing import TypedDict, List
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

USER_URL = "http://localhost:5100"


class UploadBody(TypedDict):
    """upload body typings"""
    post_content: str
    post_location: str
    post_images: List[str]


@app.route("/upload/<string:uid>", method=["POST"])
def upload_post(uid: str) -> None:
    """complex microservice to upload post"""
    try:
        data: UploadBody = request.get_json()
        content, location, images = data["post_content"], data["post_location"], data["post_images"]
        is_sfw = check_content(content)
        try:
            if is_sfw:
                pass
            else:
                email, username = get_user_email_name(uid)
                send_content_warning(email, username)

        except Exception as e:
            print(e)
            return jsonify({"code": 500, "message": "there was an error on the server"}), 500

    except KeyError:
        return jsonify({"code": 400, "message": "Post data not formatted correctly"}), 400


def check_content(text: str) -> bool:
    """sends api request to NLP analyser"""
    return False


def send_content_warning(email: str, username: str) -> None:
    """publishes content warning message to rabbitmq"""
    return


def get_user_email_name(uid: str) -> tuple:
    """gets user information from uid"""
    user_info_route = f"{USER_URL}/user/{uid}"
    response = get(user_info_route, timeout=5000)
    data = response.json()["data"]
    return data["user email"], data["username"]
