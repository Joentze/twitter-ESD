"""complex microservice to read posts"""
import os
from typing import List
from datetime import datetime
from requests import get
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)


POSTS_URL = "http://localhost:5101"
COMMENTS_URL = "http://localhost:5102"
LIKES_URL = "http://localhost:5103"
FOLLOWS_URL = "http://localhost:5104"
POST_IMAGE_URL = "http://localhost:5111"


@app.route("/read_posts/<string:uid>", methods=['GET'])
def read_posts(uid: str):
    """returns posts of following"""
    try:
        # Send a GET request to retrieve follows information
        request_route = f"{FOLLOWS_URL}/follow/{uid}"
        follows_response = get(
            request_route, timeout=5000)
        followings = follows_response.json()["data"]
        all_following_posts = []

        # gets the post of followings
        for following in followings:
            get_post_request_route = f"{POSTS_URL}/userPosts/{following}"
            post_following_response = get(get_post_request_route, timeout=5000)
            following_posts = post_following_response.json()["data"]
            all_following_posts += following_posts

        # gets and sorts the comments within each post
        sorted_posts = sort_content_by_date("date posted", all_following_posts)
        for idx, post in enumerate(sorted_posts):
            post_id = post["post id"]
            comments = get_sorted_comments(post_id)
            likes = get_likes(post_id)
            images = get_post_images(post_id)
            sorted_posts[idx] = {
                **post, "comments": comments, "likes": likes, "images": images}

        return jsonify({
            "code": 200,
            "data": sorted_posts
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Internal server error: " + str(e)
        }), 500


def get_sorted_comments(post_id: str):
    """get all comments sorted by date"""
    comment_post_route = f"{COMMENTS_URL}/comment/{post_id}"
    response = get(comment_post_route, timeout=5000)
    comments = response.json()["data"]
    return sort_content_by_date("date commented", comments)


def get_likes(post_id: str):
    """gets all likes on post"""
    like_post_route = f"{LIKES_URL}/like/{post_id}"
    response = get(like_post_route, timeout=5000)
    likes = response.json()["data"]
    return likes


def get_post_images(post_id: str):
    """gets all images on post"""
    post_image_route = f"{POST_IMAGE_URL}/postImage/{post_id}"
    response = get(post_image_route, timeout=5000)
    images = response.json()["data"]
    return images


def sort_content_by_date(key: str, items: List[object]):
    """sorts objects by date"""
    return sorted(items, key=lambda item: datetime.strptime(
        item[key], '%a, %d %b %Y %H:%M:%S %Z'), reverse=True)


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for reading posts...")
    app.run(host="0.0.0.0", port=5120, debug=True)
