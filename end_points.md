## Auth Routes

### __/register/__

#### Methods: POST  

- Arguments: None  
- Description: Creates a new user in the database  
- Authentication: none
- Headers-Authorization: Anyone can register as a new user, the default is_admin value is false. 
<br>
<br>

- Request Body:

```JSON
{     
    "first_name":"Nick",
    "last_name":"Liu",
    "email":"000000@aaa.com",
    "password":"123Abc!!",
    "gender_id":"1"
}
```

- Request response:

 ```JSON
{
    "email": "000000@aaa.com",
    "first_name": "Nick",
    "gender": {
        "name": "male"
    },
    "id": 7,
    "last_name": "Liu"
}
```

If password not meet the requirements:  

```JSON
{
    "error": {
        "password": [
            "Password should contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long"
        ]
    }
}
```

If email already taken by another user:  

```JSON
{
    "error": "email address is already in use"
}
```

If gender_id not in the database:
```JSON
{
    "error": "This gender_id doesn't exist, please view gender and select another."
}
```

### __/login/__

#### Methods: POST  

- Arguments: None
- Description: user login and receive token
- Authentication: none
- Headers-Authorization: none
<br>
<br>

- Request Body:

```JSON
{     
    "email":"123456@aaa.com",
    "password":"123456"
}
```

- Request response:

 ```JSON
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NzkxODkyNCwianRpIjoiOGI2NmFiYmItMmRiOC00ODM3LTg5MGItZjM0MjNjNWJlNTA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjg3OTE4OTI0LCJleHAiOjE2ODgwMDUzMjR9.mlApW0R2QUuGIVA-1Cfkz7uxkr5If54HotG_IQgqd7M",
    "welcome user": {
        "email": "123456@aaa.com",
        "first_name": "James",
        "gender": {
            "name": "male"
        },
        "gender_id": 1,
        "id": 2,
        "last_name": "Bond"
    }
}
```

If email or password not correct:
```JSON
{
    "error": "invalid email address or password"
}
```
If email or password not provided:
```JSON
{
    "error": "Email and password are required"
}
```

### __/change_password/__

#### Methods: POST  

- Arguments: None
- Description: user change the password
- Authentication: @jwt_required()
- Headers-Authorization: The Bear Token got when login
<br>
<br>

- Request Body:

```JSON   
{
    "old_password":"123456",
    "new_password":"123Cba!!!"
}
```

- Request response:

 ```JSON
{
    "message": "Password has been updated successfully."
}
```

If old password not correct:
```JSON
{
    "error": "Old password is incorrect."
}
```

If old or new password are not provided:
```JSON
{
    "error": "Old and new passwords are required."
}
```

### __/users/__

#### Methods: GET

- Arguments: None
- Description: Admin can access all users information
- Authentication: @jwt_required()
- Headers-Authorization: Only admin Bear Token valid
- Request Body: None

- Request response:

 ```JSON
[
    {
        "email": "654321@aaa.com",
        "first_name": "Jason",
        "gender": {
            "name": "male"
        },
        "gender_id": 1,
        "id": 3,
        "last_name": "Bourne"
    },
    {
        "email": "222222@aaa.com",
        "first_name": "Alice",
        "gender": {
            "name": "female"
        },
        "gender_id": 2,
        "id": 4,
        "last_name": "Abernathy"
    },
    {
        "email": "333333@aaa.com",
        "first_name": "Morgan",
        "gender": {
            "name": "intersex"
        },
        "gender_id": 3,
        "id": 5,
        "last_name": "Carpenter"
    }
]
```

If unauthorized:
```JSON
{
    "error": "401 Unauthorized: You must be an admin"
}
```


## Genders Routes
### __/genders/__

#### Methods: GET 

- Arguments: None  
- Description: view all gender object 
- Authentication: none
- Headers-Authorization: None. Anyone can view existing gender objects.
- Request Body:None


- Request response:

 ```JSON
[
    {
        "id": 1,
        "name": "male"
    },
    {
        "id": 2,
        "name": "female"
    },
    {
        "id": 3,
        "name": "intersex"
    },
    {
        "id": 4,
        "name": "unidentified"
    }
]
```

### __/genders/__

#### Methods: POST

- Arguments: None  
- Description: create a new gender object
- Authentication: @jwt_required()
- Headers-Authorization: The user's Bear Token
<br>
<br>

- Request Body:
```JSON
{
    "name":"unisex"
}
```


- Request response:

 ```JSON
{
    "id": 6,
    "name": "unisex"
}
```

If the gender already exist in database:  

```JSON
{
    "error": "gender already exist"
}
```

### __/genders/my_gender__

#### Methods: PUT, PATCH

- Arguments: None  
- Description: users edit their gender
- Authentication: @jwt_required()
- Headers-Authorization: The user's Bear Token
<br>
<br>

- Request Body:
```JSON
{
    "gender_id":"6"
}

```


- Request response:

 ```JSON
{
    "email": "123456@aaa.com",
    "first_name": "James",
    "gender": {
        "name": "unisex"
    },
    "gender_id": 6,
    "id": 2,
    "last_name": "Bond"
}
```

If the gender_id doesn't exist in database:  

```JSON
{
    "error": "Gender_id not exist"
}
```

### __/genders/\<int:gender_id\>__

#### Methods: PUT, PATCH

- Arguments: gender_id 
- Description: admin can edit gender name
- Authentication: @jwt_required()
- Headers-Authorization: The admin's Bear Token
<br>
<br>

- Request Body:
```JSON
{
    "name":"changed"
}
```

- Request response:

 ```JSON
{
    "id": 6,
    "name": "changed"
}
```

If the gender_id doesn't exist in database:  

```JSON
{
    "error": "gende_id_ not found"
}
```

## Hobbies Routes
### __/hobbies/__

#### Methods: GET 

- Arguments: None  
- Description: view all hobby objects
- Authentication: none
- Headers-Authorization: None. Anyone can view existing hobby objects.
- Request Body:None


- Request response:

 ```JSON
[
    {
        "id": 1,
        "name": "basketball"
    },
    {
        "id": 2,
        "name": "football"
    },
    {
        "id": 3,
        "name": "tennis"
    },
    {
        "id": 4,
        "name": "borad game"
    }
]
```

### __/hobbies/__

#### Methods: POST

- Arguments: None  
- Description: create a new hobby 
- Authentication: @jwt_required()
- Headers-Authorization: None
- Request Body:
```JSON
{
    "name":"coding"
}
```
- Request response:

 ```JSON
{
    "id": 7,
    "name": "coding"
}
```

If hobby already exists in database:  

```JSON
{
    "error": "hobby already exists"
}
```


### __/hobbies/\<int:hobby_id\>__

#### Methods: PUT, PATCH

- Arguments: id
- Description: Admin can edit hobby's name
- Authentication: @jwt_required()
- Headers-Authorization: admin's Bearer token
- Request Body: None
<br>
<br>
- Request response:

 ```JSON
{
    "id": 7,
    "name": "sleeping"
}
```

If hobby_id doesn't exist in database:  

```JSON
{
    "error": "hobby_id not found"
}
```

### __/hobbies/\<int:hobby_id\>__

#### Methods: DELETE

- Arguments: id
- Description: Admin can delete a hobby and related objects
- Authentication: @jwt_required()
- Headers-Authorization: admin's Bearer token
- Request Body: None

- Request response:

 ```JSON
{
    "message": "Hobby deleted"
}
```

If hobby_id doesn't exist in database:  
```JSON
{
    "error": "hobby_id not found"
}
```

## Users_have_hobbies Routes

### __/users_have_hobbies/view/__

#### Methods: GET 

- Arguments: None  
- Description: users can view all users' hobbies'
- Authentication: @jwt_required()
- Headers-Authorization: Bearer token
- Request Body: None


- Request response:

 ```JSON
[
    {
        "hobbies": {
            "name": "basketball"
        },
        "hobby_id": 1,
        "id": 1,
        "users": {
            "first_name": "James",
            "id": 2,
            "last_name": "Bond"
        }
    },
    {
        "hobbies": {
            "name": "football"
        },
        "hobby_id": 2,
        "id": 2,
        "users": {
            "first_name": "Jason",
            "id": 3,
            "last_name": "Bourne"
        }
    }
]
```

### __/users_have_hobbies/mine/__

#### Methods: GET

- Arguments: None
- Description: users can view their own hobbies
- Authentication: @jwt_required()
- Headers-Authorization: Bearer token
- Request Body: None

- Request response:

 ```JSON
[
    {
        "hobbies": {
            "name": "basketball"
        },
        "hobby_id": 1,
        "id": 1,
        "users": {
            "first_name": "James",
            "id": 2,
            "last_name": "Bond"
        }
    }
]
```

### __/users_have_hobbies/have/__

#### Methods: POST

- Arguments: None
- Description: users can link them to a new hobby
- Authentication: @jwt_required()
- Headers-Authorization: user's Bearer token
- Request Body: 
```JSON
{
    "hobby_id":"2"
}
```

- Request response:

 ```JSON
{
    "hobbies": {
        "name": "football"
    },
    "id": 9,
    "users": {
        "first_name": "James",
        "id": 2,
        "last_name": "Bond"
    }
}
```

If the user already has this hobby:
```JSON
{
    "error": "You already has this hobby!"
}
```

If hobby_id doesn't exist in database:  
```JSON
{
    "error": "This hobby_id doesn't exist, please select another or create one."
}
```


### __/users_have_hobbies/\<user_has_hobby_id\>/__

#### Methods: DELETE

- Arguments: id
- Description: admin or owner can delete object
- Authentication: @jwt_required()
- Headers-Authorization: Bearer token of admin or owner 
- Request Body: None
<br>
<br>
- Request response:

 ```JSON
{
    "message": "You don't have this hobby anymore"
}
```

If unauthorized:
```JSON
{
    "error": "401 Unauthorized: You must be an admin or the owner"
}
```

If the hobby_id doesn't exist in database:  
```JSON
{
    "error": "Item not found"
}
```

### __/users_have_hobbies/hobby_users/\<int:h_id\>/__

#### Methods: GET

- Arguments: id
- Description: users can view all the users who have the particular hobby
- Authentication: @jwt_required()
- Headers-Authorization: Bearer token
- Request Body: None
<br>
<br>
- Request response:

 ```JSON
[
    {
        "hobbies": {
            "name": "tennis"
        },
        "id": 3,
        "users": {
            "first_name": "Alice",
            "id": 4,
            "last_name": "Abernathy"
        }
    },
    {
        "hobbies": {
            "name": "tennis"
        },
        "id": 12,
        "users": {
            "first_name": "James",
            "id": 2,
            "last_name": "Bond"
        }
    }
]
```


If the hobby_id doesn't exist in database:
```JSON
{
    "error": "This hobby_id doesn't exist."
}
```

If no user has this hobby:
```JSON
{
    "message": "No one has this hobby yet."
}
```

### __/users_have_hobbies/hobby_genders/\<int:g_id\>/__

#### Methods: GET

- Arguments: id
- Description: users can view all the hobbies that one particluar gender have
- Authentication: @jwt_required()
- Headers-Authorization: Bearer token
- Request Body: None

- Request response:

 ```JSON
[
    "tennis",
    "football"
]
```

If the gender_id doesn't exist in database:
```JSON
{
    "message": "This gender_id not exist."
}
```

If no user has this gender_id:
```JSON
{
    "message": "No user has this gender yet."
}
```

If this gender_id has no hobbies:
```JSON
{
    "message": "This gender has no hobby yet."
}
```

