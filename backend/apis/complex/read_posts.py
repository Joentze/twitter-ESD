from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

follows_URL = "http://localhost:5104/follows"
posts_URL = "http://localhost:5101/posts"

@app.route("/read_posts", methods=['GET'])
def read_posts():
    try:
        # Send a GET request to retrieve follows information
        print('\n-----Invoking follows microservice-----')
        follows_response = requests.get(follows_URL)
        follows_data = follows_response.json().get("data", {}).get("follows", [])
        print('follows_response:', follows_data)

        if follows_response.status_code != 200:
            # Error handling if the follows microservice call fails
            return jsonify({
                "code": follows_response.status_code,
                "message": "Failed to retrieve follows information"
            }), follows_response.status_code

        # Construct a dictionary to store followers for each user
        followers_dict = {}
        for follow in follows_data:
            follower_id = follow.get("follower id")
            followed_id = follow.get("followed id")
            if followed_id not in followers_dict:
                followers_dict[followed_id] = []
            followers_dict[followed_id].append(follower_id)

        print(followers_dict)
    
        # Retrieve posts for followers of each user
        follower_posts = {}
        for user_id, follower_ids in followers_dict.items():
            user_follower_posts = []
            for follower_id in follower_ids:
                follower_posts_response = requests.get(f"{posts_URL}/userPosts/{follower_id}")
                if follower_posts_response.status_code != 200:
                    # Error handling if the posts microservice call fails
                    return jsonify({
                        "code": follower_posts_response.status_code,
                        "message": f"Failed to retrieve posts for follower {follower_id}"
                    }), follower_posts_response.status_code
                follower_posts_data = follower_posts_response.json().get("data", [])

                # Append follower's posts to user_follower_posts
                user_follower_posts.extend(follower_posts_data)

            # Sort user_follower_posts by date
            user_follower_posts.sort(key=lambda x: x.get("date_posted", ""), reverse=True)

            # Store sorted posts for followers of user_id
            follower_posts[user_id] = user_follower_posts

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
    app.run(host="0.0.0.0", port=5105, debug=True)



