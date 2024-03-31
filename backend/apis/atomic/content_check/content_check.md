# Content Check API

**Port** : `5108`

## Check the content

Used for text analysis to determine if content is safe for work

**URL** : `/post/validate`  
**Method** : `GET`  
**Auth required** : NO

**Data constraints** :

```json
{
  "inputs": "[post content]"
}
```

**Data Example**

```json
{
  "inputs": ["This is a new post"]
}
```

### Success Response

**Condition** : If content is not safe for work.
**Code** : `200 OK`  
**Content Example**

```json
{
  "code": 200,
  "sfw": false
}
```

**Condition** : If content is safe for work.
**Code** : `200 OK`  
**Content Example**

```json
{
  "code": 200,
  "sfw": true
}
```

### Error Response

**Condition** : If content is not safe for work.
**Code** : `500`  
**Content Example** :

```json
{
  "code": 500,
  "message": "There was an error on the server"
}
```
