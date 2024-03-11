# Assets

**Port** : `5105`

## Posts Image to Minio

Used to upload images.

**URL** : `/upload`  
**Method** : `POST`  
**Auth required** : Yes

### Success Response

**Code** : `201 OK`  
**Content Example**

```json
{
  "code": 201,
  "data": {
    "object_name": "a93de9fa-5b52-4006-84aa-68238f3bca04.png"
  }
}
```

### Error Response

**Condition** : Failure to upload image to Minio bucket  
**Code** : `500 Server Error`  
**Content Example** :

```json
{
  "code": 500,
  "message": "There was an error with uploading object to bucket"
}
```
