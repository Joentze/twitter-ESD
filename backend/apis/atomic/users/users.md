# Users  
**Port** : `5100`  

## Get All Users  
Used to get details of all registered users    
  
**URL** : `/users/`    
**Method** : `GET`    
**Auth required** : NA  
  
### Success Response  
**Code** : `200 OK`    
**Content Example**    
```json  
{  
    "code": 200,  
    "data": {  
        "users": [  
            {  
                "is user private": 0,  
                "user created on": "Thu, 08 Feb 2024 12:00:00 GMT",  
                "user email": "user1@example.com",  
                "user id": "user1_uid",  
                "username": "user1"  
            },  
            ...
        ]  
    }  
}  
```
  
### Error Response  
**Condition** : If there are no registered users in the database.    
**Code** : `400 BAD REQUEST`    
**Content Example** :    
```json  
{  
    "code": 404,  
    "message": "No users found!"  
}  
```
  
## Get User By UID  
Used to get details of a registered user    
  
**URL** : `/user/uid/`    
**Method** : `GET`    
**Auth required** : YES    
  
### Success Response  
**Code** : `200 OK`    
**Content Example**    
```json  
{  
    "code": 200,  
    "data": {  
        "is user private": 0,  
        "user created on": "Thu, 08 Feb 2024 12:00:00 GMT",  
        "user email": "user1@example.com",  
        "user id": "user1_uid",  
        "username": "user1"  
    }  
}  
```
  
### Error Response  
**Condition** : Requested user cannot be found  
**Code** : `400 BAD REQUEST`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "User not found."  
}  
```
  
## Create New User  
Creating a new user  
  
**URL** : `/user/uid/`  
**Method** : `POST`  
**Auth required** : NO  
  
**Data constraints**  
```json  
{  
    "username": "[valid, unique username]",  
    "email": "[valid email address]"  
}  
```
  
**Data example**  
```json  
{  
    "username": "user1",  
    "email": "user1@example.com"  
}  
```
  
## Success Response  
**Code** : `201 CREATED`    
**Content Example**    
```json  
{  
    "code": 201,  
    "data": {  
        "is user private": 0,  
        "user created on": "Mon, 08 Feb 2024 12:00:00 GMT",  
        "user email": "user5@example.com",  
        "user id": "user5_uid",  
        "username": "user5"  
    }  
}  
```
  
## Error Response  
**Condition** : If username or email is already used by another user.    
**Code** : `400 BAD REQUEST`    
**Content Example** :    
```json  
{  
    "code": 400,  
    "message": [  
        "Username user5 already exists",  
        "User with email address user5@example.com already exists"  
    ]  
}  
```
  
## Update User Details  
Updating user details  
  
**URL** : `/user/uid/`  
**Method** : `PUT`  
**Auth required** : YES  
  
**Data constraints**  
each of the following are optional  
```json  
{  
    "username": "[valid, unique username]",  
    "email": "[valid email address]",  
    "is_private": "[0, 1]"  
}  
```
  
**Data Example**  
```json  
{  
    "username": "user1",  
    "email": "user1@example.com"  
}  
```
  
### Success Response  
**Code** : `200 OK`    
**Content Example**    
```json  
{  
    "code": 201,  
    "data": {  
        "is user private": 0,  
        "user created on": "Mon, 08 Feb 2024 12:00:00 GMT",  
        "user email": "user5@example.com",  
        "user id": "user5_uid",  
        "username": "user5"  
    }  
}  
```
  
### Error Response  
**Condition** : If user with requested UID is not found.    
**Code** : `404 NOT FOUND`    
**Content Example** :    
```json  
{  
    "code": 404,  
    "message": "User not found"  
}  
```
  
## Delete User  
Deleting a user  
  
**URL** : `/user/uid`  
**Method** : `DELETE`  
**Auth required** : YES  
  
### Success Response  
**Code** : `204 NO CONTENT`  
**Content Example** :  
```json  
{  
    "code": 204,  
    "message": "User deleted successfully"  
}  
```
  
### Error Response  
**Condition** : If user with provided UID is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "User not found."  
}  
```
