# Posts  
**Port** : `5101`  

## Get All Posts  
Used to get details of all posts    
  
**URL** : `/posts/`    
**Method** : `GET`    
**Auth required** : NA  
  
### Success Response  
**Code** : `200 OK`    
**Content Example**    
```json  
{  
    "code": 200,  
    "data": {  
        "posts": [  
            {  
                "date posted": "Thu, 08 Feb 2024 12:10:00 GMT",  
                "post content": "Hello World!",  
                "post id": "post1_id",  
                "post location": "New York",  
                "poster id": "user1_uid"  
            },  
            ...
        ]  
    }  
}  
```
  
### Error Response  
**Condition** : If there are no posts in the database.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "No posts found!"  
}  
```
  
## Get Post By Post ID  
Used to get details of a post by its ID  
  
**URL** : `/post/post_id`  
**Method** : `GET`  
**Auth required** : NA  
  
### Success Response  
**Code** : `200 OK`  
**Content Example**  
```json  
{
    "code": 200,
    "data": {
        "date posted": "Thu, 08 Feb 2024 12:10:00 GMT",
        "post content": "Hello World!",
        "post id": "post1_id",
        "post location": "New York",
        "poster id": "user1_uid"
    }
}
```
  
### Error Response  
**Condition** : Requested post cannot be found  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Post not found."  
}  
```
  
## Create New Post  
Creating a new post  
  
**URL** : `/post/poster_uid`  
**Method** : `POST`  
**Auth required** : YES  
  
**Data constraints** :  
```json  
{  
    "post_content": "[post content]",  
    "post_location": "[post location]"  
}  
```
**Data Example**  
```json  
{  
    "post_content": "This is a new post",  
    "post_location": "New York"  
}  
```
  
### Success Response  
**Code** : `201 CREATED`  
**Content Example**  
  
```json  
{  
    "code": 201,  
    "data": {
        "date posted": "Mon, 12 Feb 2024 15:13:00 GMT",
        "post content": "This is a new post",
        "post id": "4d5225f4-217d-4660-b596-0e6802786c77",
        "post location": "California",
        "poster id": "user4_uid"
    }
}  
```
  
### Error Response  
**Condition** : If an error occurs while creating the post.  
**Code** : `500 INTERNAL SERVER ERROR`  
**Content Example** :  
```json  
{  
    "code": 500,  
    "message": "An error occurred creating the post."  
}  
```
  
## Update Post  
Updating post details  
  
**URL** : `/post/post_id`  
**Method** : `PUT`  
**Auth required** : YES  
  
**Data constraints**  
```json  
{  
    "post_content": "[post content]",  
    "post_location": "[post location]"  
}  
```
  
### Success Response  
**Code** : `200 OK`  
**Content Example** :  
```json  
{  
    "code": 200,  
    "data": {
        "date posted": "Thu, 08 Feb 2024 12:10:00 GMT",
        "post content": "This is post has been updated!",
        "post id": "post1_id",
        "post location": "updated location",
        "poster id": "user1_uid"
    }
}  
```
  
### Error Response  
**Condition** : If post with provided ID is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Post not found."  
}  
```
  
## Delete Post  
Deleting a post  
  
**URL** : `/post/post_id`  
**Method** : `DELETE`  
**Auth required** : NO  
  
### Success Response  
**Code** : `204 NO CONTENT`  
**Content Example** :  
```json  
{  
    "code": 204,  
    "message": "Post deleted successfully"  
}  
```
  
### Error Response  
**Condition** : If post with provided ID is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Post not found."  
}  
```
