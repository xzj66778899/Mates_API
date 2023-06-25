from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required


hobbies_bp = Blueprint('hobbies',__name__, url_prefix = '/hobbies')


# view all hobbies
@hobbies_bp.route('/')
@jwt_required()
def all_genders():
   stmt = db.select(Hobby)
   genders = db.session.scalars(stmt)
   return HobbySchema(many = True).dump(genders)


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
  


# admin can delete a hobby and related user_has_hobby
@hobbies_bp.route('/<int:hobby_id>', methods=['DELETE'])
@jwt_required()
def delect_card(hobby_id):
  admin_required()
  stmt = db.select(Hobby).filter_by(id = hobby_id)
  hobby = db.session.scalar(stmt)
  if hobby:
    db.session.delete(hobby)
    db.session.commit()
    return {'message':'Hobby deleted'}, 200
  else:
    return {'error': 'Hobby not found'}, 404