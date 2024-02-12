# Comments  
**Port** : `5102`  
  
## Get All Comments  
Used to get details of all comments.  
  
**URL** : `/comments`  
**Method** : `GET`  
**Auth required** : No  
  
### Success Response  
**Code** : `200 OK`  
**Content Example**  
```json  
{  
    "code": 200,  
    "data": {  
        "comments": [  
            {  
                "comment id": "comment1_id",  
                "commenter uid": "user1_uid",  
                "content": "Great!",  
                "date commented": "Thu, 08 Feb 2024 12:31:00 GMT",  
                "post id": "post3_id"  
            },  
            ...
        ]  
    }  
}  
```
  
### Error Response  
**Condition** : If there are no comments in the database.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "No one is commenting each other!"  
}  
```
  
## Get Comments By Post ID  
Used to get details of comments by post ID.  
  
**URL** : `/comment/post_id`  
**Method** : `GET`  
**Auth required** : NO  
  
### Success Response  
**Code** : `200 OK`  
**Content Example** :  
```json  
{  
    "code": 200,  
    "data": [  
        {  
            "comment id": "comment3_id",  
            "commenter uid": "user3_uid",  
            "content": "Awesome!",  
            "date commented": "Thu, 08 Feb 2024 12:33:00 GMT",  
            "post id": "post1_id"  
        }  
        ...
    ]  
}  
```
  
### Error Response  
**Condition** : If the post has no comments or post is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Post has no comments"  
}  
```
  
## Create Comment  
Creating a new comment.  
  
**URL** : `/comment/post_id`  
**Method** : `POST`  
**Auth required** : YES  
  
**Data constraints** :  
```json  
{  
    "commenter_uid": "[valid commenter_uid]",  
    "content": "[content]"  
}  
```
**Data Example** :  
```json  
{  
    "content": "This is a new comment",  
    "commenter_uid": "user4_uid"  
}  
```
  
### Success Response  
**Code** : `201 CREATED`  
**Content Example** :  
```json  
{  
    "code": 201,  
    "data": {  
        "comment id": "b9c83491-e800-47b8-b1bb-fb939bbbbdc6",  
        "commenter uid": "user4_uid",  
        "content": "This is a new comment",  
        "date commented": "Mon, 12 Feb 2024 15:21:43 GMT",  
        "post id": "post1_id"  
    }  
}  
```
  
### Error Response  
**Condition** : If an error occurs while creating the comment.  
**Code** : `500 INTERNAL SERVER ERROR`  
**Content Example** :  
```json  
{  
    "code": 500,  
    "message": "An error occurred creating the comment."  
}  
```
  
### Update Comment  
Updating comment details.  
  
**URL** : `/comment/post_id`  
**Method** : PUT  
**Auth required** : YES  
  
**Data constraints** :  
```json  
{  
    "comment_id": "[comment_id]",  
    "content": "[content]"  
}  
```
  
**Data Example** :  
```json  
{  
    "comment_id": "comment3_id",  
    "content": "content updated"  
}  
```
  
### Success Response  
**Code** : `201 CREATED`  
**Content Example** :  
```json  
{  
    "code": 201,  
    "data": {  
        "comment id": "comment3_id",  
        "commenter uid": "user3_uid",  
        "content": "content updated",  
        "date commented": "Mon, 12 Feb 2024 15:23:59 GMT",  
        "post id": "post1_id"  
    }  
}  
```
  
### Error Response  
**Condition** : If comment with provided ID is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Comment not found."  
}  
```
  
## Delete Comment  
Deleting a comment.  
  
**URL** : `/comment/post_id`  
**Method** : `DELETE`  
**Auth required** : YES  
  
**Data constraints** :  
```json  
{  
    "comment_id": "[comment_id]"  
}  
```
**Data Example** :  
```json  
{  
    "comment_id": "comment1_id"  
}  
```
  
### Success Response  
**Code** : `204 NO CONTENT`  
**Content Example** :  
```json  
{  
    "code": 204,  
    "message": "Comment deleted successfully"  
}  
```
  
### Error Response  
**Condition** : If the comment with provided ID is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Comment not found"  
}  
```
