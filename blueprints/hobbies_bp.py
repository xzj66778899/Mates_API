from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required


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


# update a hobby
@hobbies_bp.route('/<int:hobby_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(hobby_id):
  admin_required()
  stmt = db.select(Hobby).filter_by(id = hobby_id)
  hobby = db.session.scalar(stmt)
  hobby_info = HobbySchema().load(request.json)
  if hobby:
    hobby.name = hobby_info.get('name',hobby.name)
    db.session.commit()
    return HobbySchema().dump(hobby)
  else:
    return {'error': 'Hobby not found'}, 404