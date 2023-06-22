from init import db,ma
from marshmallow import fields


class Hobby(db.Model):
    __tablename__ = 'hobbies'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
   
    users_have_hobbies = db.relationship('User_has_hobby', back_populates = 'hobbies')

class HobbySchema(ma.Schema):
    class meta:
        fields = ('id', 'name')

