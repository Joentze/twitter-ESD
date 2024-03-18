const express = require('express');
const { invokeHttp } = require('./invokes');

const app = express();
const port = 5120;

app.use(express.json());

const API_URL = process.env.API_URL;
const FOLLOW_URL = `${API_URL}/follow`;
const POST_URL = `${API_URL}/post/user_get`;

app.get("/read_posts", async (req, res) => {
    try {
        const user_uid = req.headers.uid;

        if (!user_uid) {
            return res.status(400).json({
                "code": 400,
                "message": "User ID not provided in the request headers"
            });
        }

        const new_followsURL = `${FOLLOW_URL}/${user_uid}`;
        const follows_response = await invokeHttp(new_followsURL, 'GET');

        if (!follows_response || follows_response.code !== 200) {
            return res.status(500).json({
                "code": 500,
                "message": "Failed to retrieve follows information"
            });
        }

        const followers_dict = {};
        followers_dict[user_uid] = follows_response.data || [];

        let follower_posts = [];
        for (const user_id in followers_dict) {
            const follower_ids = followers_dict[user_id];
            for (const follower_id of follower_ids) {
                const new_PostsURL = `${POST_URL}/${follower_id}`;
                const follower_posts_response = await invokeHttp(new_PostsURL, 'GET');
                if (follower_posts_response.code === 200) {
                    follower_posts = follower_posts.concat(follower_posts_response.data || []);
                }
            }
        }

        if (follower_posts.length === 0) {
            return res.status(500).json({
                "code": 500,
                "message": "Failed to retrieve posts information"
            });
        }

        follower_posts.sort((a, b) => new Date(b["date posted"]) - new Date(a["date posted"]));

        return res.status(200).json({
            "code": 200,
            "data": follower_posts
        });
    } catch (error) {
        return res.status(500).json({
            "code": 500,
            "message": "Internal server error: " + error.message
        });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

