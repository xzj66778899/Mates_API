from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity


hobbies_bp = Blueprint('hobbies',__name__, url_prefix = '/hobbies')


# create a new hobby
@hobbies_bp.route('/', methods = ['POST'])
@jwt_required()
def create_hobby():
  hobby_info = HobbySchema().load(request.json)
  hobby = Hobby(
    name = hobby_info['name'].lower(),         
  )
  db.session.add(hobby)
  db.session.commit()

  return HobbySchema().dump(hobby), 201
