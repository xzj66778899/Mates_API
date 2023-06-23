from init import db,ma
from marshmallow import fields


class Gender(db.Model):
    __tablename__ = 'genders'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
   

    users = db.relationship('User', back_populates = 'gender', cascade = 'all,delete')


class GenderSchema(ma.Schema):
    class meta:
        fields = ('id', 'name')

