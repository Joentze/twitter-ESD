from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import sys

from requests import get
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

follows_URL = "http://localhost:5104"
posts_URL = "http://localhost:5101"


@app.route("/read_posts/<string:uid>", methods=['GET'])
def read_posts(uid: str):
    """returns posts of following"""
    try:
        # Send a GET request to retrieve follows information
        print('\n-----Invoking follows microservice-----')
        request_route = f"{follows_URL}/follow/{uid}"
        follows_response = get(
            request_route, timeout=5000)
        followings = follows_response.json()["data"]
        all_following_posts = []
        for following in followings:
            get_post_request_route = f"{posts_URL}/userPosts/{following}"
            post_following_response = get(get_post_request_route, timeout=5000)
            following_posts = post_following_response.json()["data"]
            all_following_posts += following_posts

        sorted_posts = sorted(all_following_posts, key=lambda item: datetime.strptime(
            item['date posted'], '%a, %d %b %Y %H:%M:%S %Z'), reverse=True)

        return jsonify({
            "code": 200,
            "data": sorted_posts
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Internal server error: " + str(e)
        }), 500


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for reading posts...")
    app.run(host="0.0.0.0", port=5120, debug=True)
