# PostPostImages API  
**Port** : `5111`  
  
## Get All Post Images  
Used to get details of all post images.  
  
**URL** : `/postImages`  
**Method** : `GET`  
**Auth required** : NO  
  
### Success Response  
**Code** : `200 OK`  
**Content Example**  
```json  
{  
    "code": 200,  
    "data": {  
        "postImage": [  
            {  
                "object id": "object_id_1",  
                "post id": "post_id_1",  
                "date used": "Thu, 08 Feb 2024 12:01:00 GMT"  
            },  
            ...  
        ]  
    }  
}  
```
  
### Error Response  
**Condition** : If there are no post images in the database.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "No postImage found!"  
}  
```
  
## Find Images By Post ID  
Used to get details of post images by post ID.  
  
**URL** : `/postImage/post_id`  
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
            "object id": "image1_id",  
            "post id": "post1_id",  
            "date used": "Thu, 08 Feb 2024 12:01:00 GMT"  
        },  
        ...  
    ]  
}  
```
  
### Error Response  
**Condition** : If no post images are found for the given post ID.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "PostImage not found."  
}  
```
  
## Create Post Image  
Creating a new post image.  
  
**URL** : `/postImage/object_id`  
**Method** : `POST`  
**Auth required** : YES  
  
### Success Response  
**Code** : `201 CREATED`  
**Content Example** :  
```json  
{  
    "code": 201,  
    "data": {  
        "object id": "image1_id",  
        "post id": "post1_id",  
        "date used": "Mon, 12 Feb 2024 15:10:21 GMT"  
    }  
}  
```
  
### Error Response  
**Condition** : If an error occurs while creating the post image.  
**Code** : `500 INTERNAL SERVER ERROR`  
**Content Example** :  
```json  
{  
    "code": 500,  
    "data": {  
        "object_id": "image1_id"  
    },  
    "message": "An error occurred creating the postImage."  
}  
```
  
## Delete Post Image  
Deleting a post image.  
  
**URL** : `/postImage/object_id`  
**Method** : `DELETE`  
**Auth required** : YES  
  
### Success Response  
**Code** : `204 NO CONTENT`  
**Content Example** :  
```json  
{  
    "code": 204,  
    "message": "PostImage deleted successfully"  
}  
```
  
### Error Response  
**Condition** : If the post image with provided object ID is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "PostImage not found."  
}  
```
