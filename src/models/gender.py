from init import db,ma
from marshmallow import fields


class Gender(db.Model):
    __tablename__ = 'genders'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable = False, unique=True)
   

    users = db.relationship('User', back_populates = 'gender')


class GenderSchema(ma.Schema):
    class Meta:
        fields = ('id','name')

