# Images API  
**Port** : `5110`  
  
## Get All Images  
Used to get details of all images.  
  
**URL** : `/images`  
**Method** : `GET`  
**Auth required** : NO  
  
### Success Response  
**Code** : `200 OK`  
**Content Example**  
```json  
{  
    "code": 200,  
    "data": {  
        "images": [  
            {  
                "date created": "Thu, 08 Feb 2024 12:40:00 GMT",  
                "object id": "image1_id",  
                "uploader uid": "user1_uid"  
            },  
            ...  
        ]  
    }  
}  
```
  
### Error Response  
**Condition** : If there are no images found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "No images found!"  
}  
```
  
## Find Images Uploaded By  
Used to find images uploaded by a specific user.  
  
**URL** : `/imageUploadedBy/uploader_uid`  
**Method** : `GET`  
**Auth required** : YES  
  
### Success Response  
**Code** : `200 OK`  
**Content Example** :  
```json  
{  
    "code": 200,  
    "data": [  
        {  
            "date created": "Thu, 08 Feb 2024 12:40:00 GMT",  
            "object id": "image1_id",  
            "uploader uid": "user1_uid"  
        },  
        ...  
    ]  
}  
```
  
### Error Response  
**Condition** : If the requested user's images are not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Image not found."  
}  
```
  
## Find Image  
Used to find an image by its object ID.  
  
**URL** : `/image/object_id`  
**Method** : `GET`  
**Auth required** : NO  
  
### Success Response  
**Code** : `200 OK`  
**Content Example** :  
```json  
{  
    "code": 200,  
    "data": {  
        "date created": "Thu, 08 Feb 2024 12:41:00 GMT",  
        "object id": "image2_id",  
        "uploader uid": "user2_uid"  
    }  
}  
```
  
### Error Response  
**Condition** : If the requested image is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Image not found."  
}  
```
  
## Create Image  
Creating a new image.  
  
**URL** : `/image/object_id`  
**Method** : `POST`  
**Auth required** : YES  
  
**Data constraints** :  
```json  
{  
    "uploader_uid": "[uploader_uid]"  
}  
```
  
### Success Response  
**Code** : `201 CREATED`  
**Content Example** :  
```json  
{  
    "code": 201,  
    "data": {  
        "date created": "Mon, 12 Feb 2024 15:44:57 GMT",  
        "object id": "image4_id",  
        "uploader uid": "user4_uid"  
    }  
}  
```
  
### Error Response  
**Condition** : If an error occurs while creating the image.  
**Code** : `500 INTERNAL SERVER ERROR`  
**Content Example** :  
```json  
{  
    "code": 500,  
    "data": {  
        "object_id": "[object_id]"  
    },  
    "message": "An error occurred creating the image."  
}  
```
  
## Delete Image  
Deleting an image.  
  
**URL** : `/image/object_id`  
**Method** : `DELETE`  
**Auth required** : YES  
  
### Success Response  
**Code** : `204 NO CONTENT`  
**Content Example** :  
```json  
{  
    "code": 204,  
    "message": "Image deleted successfully"  
}  
```
  
### Error Response  
**Condition** : If the requested image is not found.  
**Code** : `404 NOT FOUND`  
**Content Example** :  
```json  
{  
    "code": 404,  
    "message": "Image not found."  
}  
```
