# Likes API  
**Port** : `5103`  
  
## Get All Likes  
Used to get details of all likes.  
  
**URL** : `/likes`  
**Method** : `GET`  
**Auth required** : NO  
  
### Success Response  
**Code** : `200 OK`  
**Content Example**  
```json  
{  
    "code": 200,  
    "data": {  
        "likes": [  
            {  
                "date liked": "Thu, 08 Feb 2024 12:11:00 GMT",  
                "post id": "post2_id",  
                "user id": "user1_uid"  
            },  
            ...
        ]  
    }  
}  
```
  
### Error Response    
**Condition** : If there are no likes in the database.    
**Code** : `404 NOT FOUND`    
**Content Example** :    
```json    
{    
    "code": 404,    
    "message": "No one is likeing each other!"    
}  
```
  
## Get Likes By Post ID    
Used to get details of likes by post ID.  
  
**URL** : `/like/post_id`    
**Method** : `GET`    
**Auth required** : NO  
  
### Success Response    
**Code** : `200 OK`      
**Content Example** :  
```json    
{    
    "code": 200,    
    "data": [    
        "user2_uid",  
        ...
    ]    
}    
```
  
### Error Response    
**Condition** : If the post has no likes.    
**Code** : `404 NOT FOUND`    
**Content Example** :    
```json    
{    
    "code": 404,    
    "message": "Post has no likes"    
}    
```
  
## Create Like    
Creating a new like.  
  
**URL** : `/like/post_id`    
**Method** : `POST`    
**Auth required** : YES  
  
**Data constraints** :    
```json    
{    
    "uid": "[uid]"    
}    
```
**Data Example** :  
```json  
{  
    "uid": "user3_uid"  
}  
```
  
### Success Response    
**Code** : `201 CREATED`      
**Content Example**      
```json    
{    
    "code": 201,    
    "data": {  
        "date liked": "Mon, 12 Feb 2024 15:32:23 GMT",  
        "post id": "post1_id",  
        "user id": "user4_uid"  
    }  
}    
```
  
### Error Response    
**Condition** : If the post has already been liked by the user.    
**Code** : `400 BAD REQUEST`    
**Content Example** :    
```json    
{    
    "code": 400,    
    "data": {    
        "post id": "[post id]"    
    },    
    "message": "Post [post id] has already been liked by user"    
}  
```
  
## Delete Like    
  
Deleting a like.  
  
**URL** : `/like/post_id`    
**Method** : `DELETE`    
**Auth required** : YES  
  
**Data constraints** :    
```json    
{    
    "uid": "[uid]"    
}    
```
  
### Success Response    
**Code** : `204 NO CONTENT`      
**Content Example** :  
```json    
{    
    "code": 204,    
    "message": "Like deleted successfully"    
}    
```
  
### Error Response    
**Condition** : If the post is not liked by the user.    
**Code** : `404 NOT FOUND`    
**Content Example** :    
```json    
{    
    "code": 404,    
    "message": "Post is not liked by user"    
}    
```
