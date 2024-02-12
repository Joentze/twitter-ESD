# Follows  
**Port** : `5104`  
  
## Get All Follows  
Used to get details of all follows.  
  
**URL** : `/follows`  
**Method** : `GET`  
**Auth required** : NO  
  
### Success Response  
**Code** : `200 OK`  
**Content Example**  
```json  
{  
    "code": 200,  
    "data": {  
        "follows": [  
            {  
                "date followed": "Thu, 08 Feb 2024 12:01:00 GMT",  
                "followed id": "user2_uid",  
                "follower id": "user1_uid"  
            },  
            ...
        ]  
    }  
}  
```
  
### Error Response  
**Condition** : If there are no follows in the database.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "No one is following each other!"  
}  
```
  
## Get Followed Users By User ID  
Used to get details of users followed by a specific user.  
  
**URL** : `/follow/uid`  
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
        "user3_uid",  
        "user4_uid",  
        ...
    ]  
}  
```
  
### Error Response  
**Condition** : If the user is not following anyone.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "User not following anyone"  
}  
```
  
## Create Follow  
Creating a new follow.  
  
**URL** : `/follow/uid`  
**Method** : `POST`  
**Auth required** : NO  
  
### Success Response  
**Code** : 201 CREATED  
**Content Example** :  
```json  
{  
    "code": 201,  
    "data": {  
        "date followed": "Mon, 12 Feb 2024 15:10:21 GMT",  
        "followed id": "user4_uid",  
        "follower id": "user1_uid"  
    }  
}  
```
  
### Error Response  
**Condition** : If an error occurs while creating the follow.  
**Code** : `500 INTERNAL SERVER ERROR`  
**Content Example** :  
```json  
{  
    "code": 500,  
    "message": "An error occurred creating the follow."  
}  
```
  
## Delete Follow  
Deleting a follow.  
  
**URL** : `/follow/uid`  
**Method** : `DELETE`  
**Auth required** : YES  
  
### Success Response  
**Code** : `204 NO CONTENT`  
**Content Example** :  
```json  
{  
    "code": 204,  
    "message": "Follow deleted successfully"  
}  
```
  
### Error Response  
**Condition** : If the follow with provided ID is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Not following selected user."  
}  
```
