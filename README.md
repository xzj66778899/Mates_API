# ZhongjianXu_T2A2

## Table of Contents

1. [R1](#r1)
2. [R2](#r2)
3. [R3](#r3)
4. [R4](#r4)
5. [R5](#r5)
6. [R6](#r6)
7. [R7](#r7)
8. [R8](#r8)


## __R1__ 
<a name="r1"></a>
This API allows people to query the information about personal hobbies from the database by choosing different categories. 

## __R2__ 
<a name="r2"></a>
By using this API with our database, people can find those who share same hobbies with them, which can be further used to build online interest group, or combined with location services to gather offline avtivities.

## __R3__ 
<a name="r3"></a>
PostgreSQL database was used to structure the data and inentify the relationship among them. As the API functions mainly show the hobbies users share with, so a relational database is suitable for that purpose because the entities are interconnected, and by normalizing the data the database can help to ensure data consistency, thus finding and sorting the data is the advantage of the relational database.
But at the same time, it slows down the performance of the database comparing to non-relational ones.

## __R4__ 
<a name="r4"></a>
Object-Relational Mapping (ORM) acts as a bridge between relational database and object-oriented programming language.
By using SQLAlchemy in this case, we write python rather than SQL language to interact with the database, which makes data more readable and maintainable. 
The ORM also eliminates the SQL injection by the attackers because we no longer directly write SQL statements.

## __R5__ 
<a name="r5"></a>
Click and view [API End Points](docs/end_points.md)

## __R6__ 
<a name="r6"></a>
Click and view [ERD](docs/ERD.png)

## __R7__ 
<a name="r7"></a>
Flask is a lightweight framework that provides lots of third party service packages to implement the functions we want into the application. The following services are installed in this APP to expand the functionality.
### SQLAlchemy: ###
SQLAlchemy is a ORM tool that performs as a higher-level way to interact with database rather than plain database language. For example, It use Python Class with fields to define a database table and its columns. 

### Marshmallow: ###
It's a Python library that convert data types into Python data types. We created Schema class for the models then make Schema as a intermediator for getting and returning data.
For example, the following codes show how to convert a JSON data into Python object.
```
hobby_info = HobbySchema().load(request.json)
```

### Flask-Bcrypt: ###
It's a Flask extension that for hashing passwords in the database, which can protect the original plain text password even the database is hacked into. Because the hashing is a one-way road, it's not practical to decode a hashing password.
Also, it provides a function to check if the plain text password match the hashing password.

### Flask-JWT-Extended:  ###
It's a Flask extension that support JSON web tokens that commenly used for authentication in web applications. It can generate, vertificate and refresh tokens for users, as well as tracking the current user in the application.


## __R8__ 
<a name="r8"></a>
__Model user__: <br>
This model contains users information and is the parent model of 'gender'. <br>
It also has 'many to many' relationships with 'hobby' model that bridged by the 'user_has_hobby'connecting model.

```PYTHON
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    is_admin = db.Column(db.Boolean, default=False)

    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    gender = db.relationship('Gender', back_populates = 'users', cascade = 'all, delete') 

    users_have_hobbies = db.relationship('User_has_hobby')


class UserSchema(ma.Schema):
    gender = fields.Nested('GenderSchema', exclude = ['id'])
    password = fields.String(required=True, validate=Regexp(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',error='Password should contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long'))

    class Meta:
        fields = ("id",'first_name', 'password', 'last_name','email','gender','gender_id')
```

__Model gender__: <br>
This model contains gender information and it's a child model of 'user' (one to many).

```PYTHON
class Gender(db.Model):
    __tablename__ = 'genders'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable = False, unique=True)
   

    users = db.relationship('User', back_populates = 'gender', cascade = 'all,delete')


class GenderSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
```

__Model hobby__: <br>
This model contains hobby information and has 'many to many' relationships with 'user' model that bridged by the 'user_has_hobby'connecting model.

```PYTHON
class Hobby(db.Model):
    __tablename__ = 'hobbies'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
   
    users_have_hobbies = db.relationship('User_has_hobby',cascade="all,delete")

class HobbySchema(ma.Schema):
    class Meta:
        fields = ('id','name',)
```

__Model user_has_hobby__: <br>
This model is a connecting model that bridge the 'user' and 'hobby' model that have a 'many to many' relationship.

```PYTHON
class User_has_hobby(db.Model):
    __tablename__ = 'users_have_hobbies'

    id = db.Column(db.Integer, primary_key=True)
   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', back_populates = 'users_have_hobbies')

    hobby_id = db.Column(db.Integer, db.ForeignKey('hobbies.id',ondelete='CASCADE'), nullable=False)
    hobbies = db.relationship('Hobby', back_populates = 'users_have_hobbies')


class User_has_hobbySchema(ma.Schema):
    users = fields.Nested('UserSchema', exclude = ['password','email','gender','gender_id'])
    hobbies = fields.Nested('HobbySchema',exclude = ['id'])

    class Meta:
        fields = ('id','hobby_id','users','hobbies')
```


