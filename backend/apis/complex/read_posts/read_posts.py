<<<<<<< HEAD
"""complex microservice to read posts"""
import os
from typing import List
from datetime import datetime
from requests import get
from flask_cors import CORS
from flask import Flask, jsonify
=======
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import sys

import os, sys

import logging
from logging.handlers import RotatingFileHandler

import requests
from invokes import invoke_http


>>>>>>> 0f7512cd21023b30e6e2f256fe5f396b2a977e46

app = Flask(__name__)
CORS(app)

<<<<<<< HEAD

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
=======
# Configure logging
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

follows_URL = "http://host.docker.internal:8000/api/follow"
posts_URL = "http://host.docker.internal:8000/api/post/user_get"

@app.route("/read_posts", methods=['GET'])
def read_posts():
    # app.logger.info("THIS IS CALLED")
    try:
        # Send a GET request to retrieve follows information
        print('\n-----Invoking follows microservice-----')

        user_uid = request.headers.get('uid')
        # app.logger.info('test test uid')

        if not user_uid:
            return jsonify({
                "code": 400,
                "message": "User ID not provided in the request headers"
            }), 400
        
        print('printing user uid')
        print(user_uid)
        new_followsURL = follows_URL + '/' + user_uid
        follows_response = invoke_http(new_followsURL, method='GET')
        app.logger.info(follows_URL + '/' + user_uid)

        print('printing follows response')
        print(follows_response)
        print(type(follows_response))
        # follows_data = follows_response.get("data", [])
        # print('follows_response:', follows_data)
        
        # app.logger.info(follows_response)

        # Check if the response is successful
        if "code" not in follows_response or follows_response["code"] != 200:
            # Error handling if the follows microservice call fails
            # app.logger.info('test test')

            return jsonify({
                "code": follows_response.get("code", 500),
                "message": "Failed to retrieve follows information"
            }), follows_response.get("code", 500)

        # Construct a dictionary to store followers for each user
        followers_dict = {}
        followers_dict[user_uid] = follows_response.get("data", [])

        print('printing followers dict')
        print(followers_dict)

        # Retrieve posts for followers of each user

        follower_posts = []
        for user_id, follower_ids in followers_dict.items():
            print(follower_ids)
            for follower_id in follower_ids:
                print(follower_id)
                new_PostsURL = posts_URL + "/" + follower_id
                follower_posts_response = invoke_http(new_PostsURL, method='GET')
                # app.logger.info(follower_posts_response)
                if "code" not in follower_posts_response or follower_posts_response["code"] != 200:
                # Error handling if the follows microservice call fails
                    continue
                follower_posts += follower_posts_response.get("data", [])

        if not follower_posts:
            return jsonify({
                "code": follower_posts_response.get("code", 500),
                "message": "Failed to retrieve posts information"
            }), follower_posts_response.get("code", 500)

        # Sort user_follower_posts by date
        follower_posts.sort(key=lambda x: x.get("date posted", ""), reverse=True)

        print(follower_posts)
        # Return posts for followers of each user
        return jsonify({
            "code": 200,
            "data": follower_posts
>>>>>>> 0f7512cd21023b30e6e2f256fe5f396b2a977e46
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Internal server error: " + str(e)
        }), 500


<<<<<<< HEAD
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


=======
>>>>>>> 0f7512cd21023b30e6e2f256fe5f396b2a977e46
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for reading posts...")
    app.run(host="0.0.0.0", port=5120, debug=True)
<<<<<<< HEAD
=======




>>>>>>> 0f7512cd21023b30e6e2f256fe5f396b2a977e46
