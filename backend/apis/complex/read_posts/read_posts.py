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



app = Flask(__name__)
CORS(app)

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




