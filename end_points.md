## Auth Routes

### /auth/register/

#### Methods: POST  

- Arguments: None  
- Description: Creates a new user in the database  
- Authentication: none
- Headers-Authorization: Bearer {Token}- Anyone can register as a new user, the default is_admin value is false. 

- Request Body:

```JSON
{   "complex_number": 14,
    "street_number": 20,
    "street_name": "Captain Road",
    "suburb": "West End",
    "postcode": 4006,
    "users": [{
        "title": "Ms",
        "first_name": "Rachael",
        "middle_name": "Anne",
        "last_name": "Cook",
        "password": "hamAnd335*",
        "email": "test.coggfg4hhttt@bgbc.edu.au",
        "phone": "0414563531",
        "dob": "1980-09-02",
        "gender": "female"
    }]
}
```

- Request response:

 ```JSON
  {
{
    "id": 7,
    "title": "Ms",
    "first_name": "Rachael",
    "middle_name": "Anne",
    "last_name": "Cook",
    "email": "test.coggfg4hhttt@bgbc.edu.au",
    "phone": "0414563531",
    "dob": "1980-09-02",
    "gender": "female",
    "type": "Student",
    "address": {
        "id": 6,
        "complex_number": 14,
        "street_number": 20,
        "street_name": "Captain Road",
        "suburb": "West End",
        "postcode": 4006
    }
}
    }


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
