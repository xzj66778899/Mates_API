from init import db,ma
from marshmallow import fields
from marshmallow.validate import Regexp
from marshmallow.exceptions import ValidationError


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


