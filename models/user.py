from init import db,ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    is_admin = db.Column(db.Boolean, default=False)

    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    gender = db.relationship('Gender', back_populates = 'users') 

    users_have_hobbies = db.relationship('User_has_hobby', back_populates = 'users')


class UserSchema(ma.Schema):
    gender = fields.Nested('Gender')

    class meta:
        fields = ('id', 'first_name', 'last_name','email' 'password', 'is_admin', 'gender')


