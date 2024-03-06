# APIs  
Directory of microservices via Kong  
  
## Atomic Microservices  
**[Users](atomic/users/users.md)**    
Get all users: `GET /user/all`    
Get user by UID: `GET /user/uid/`    
Create new user: `POST /user/uid/`    
Update user details: `PUT /user/uid/`    
Delete user: `DELETE /user/uid/`    

**[Posts](atomic/posts/posts.md)**  
Get all posts: `GET /post/all`  
Get post by user ID: `GET /post/user_get/poster_id`  
Get post by post ID: `GET /post/post_id`  
Create new post: `POST /post/poster_uid`  
Update post: `PUT /post/post_id`  
Delete post: `DELETE /post/post_id`  

**[Comments](atomic/comments/comments.md)**  
Get all comments: `GET /comment/all`  
Get comments by user: `GET /comment/user_get/commenter_uid`  
Get comments by post: `GET /comment/post_id`  
Create new comment: `POST /comment/post_id`  
Update comment: `PUT /comment/post_id`  
Delete comment: `DELETE /comment/post_id`  

**[Likes](atomic/likes/likes.md)**  
Get all likes: `GET /like/all`  
Get likes by user: `GET /likes/user_get/uid`  
Get likes by post: `GET /like/post_id`  
Create new like: `POST /like/post_id`  
Delete like: `DELETE /like/post_id`  

**[Follows](atomic/follows/follows.md)**  
Get all follows: `GET /follow/all`  
Get user following: `GET /follow/uid`  
Create new user following: `POST /follow/uid`  
Delete user following: `DELETE /follow/uid`  

**[Images](atomic/images/images.md)**  
Get all images: `GET /images/`  
Get images from user: `GET /imageUploadedBy/uploader_uid`  
Get images by ID: `GET /image/object_id`  
Create new image: `POST /image/object_id`  
Delete image: `DELETE /image/object_id`  

**[Post Image](atomic/post_images/post_images.md)**  
Get all post images: `GET /postImages/`  
Get images of post: `GET /postImage/post_id`  
Create new post image: `POST /postImage/object_id`  
Delete post image: `DELETE /postImage/object_id`  

**[Assets](atomic/assets/assets.md)**  
Upload new image: `POST /asset/upload`  

## Complex Microservices
**[Read Posts](complex/read_posts/read_posts.md)**  
View all posts of users followed: `GET /read_posts`  
