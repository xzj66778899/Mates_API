from init import db,ma


class Hobby(db.Model):
    __tablename__ = 'hobbies'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
   
    users_have_hobbies = db.relationship('User_has_hobby',cascade="all,delete")

class HobbySchema(ma.Schema):
    class Meta:
        fields = ('id','name',)
