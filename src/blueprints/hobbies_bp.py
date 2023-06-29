from flask import Blueprint, request
from models.hobby import Hobby, HobbySchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from sqlalchemy.exc import IntegrityError

hobbies_bp = Blueprint('hobbies',__name__, url_prefix = '/hobbies')


# users can view all hobbies
@hobbies_bp.route('/')
@jwt_required()
def all_genders():
  #  select all items in hobbies table
   stmt = db.select(Hobby)
   genders = db.session.scalars(stmt)
   return HobbySchema(many = True).dump(genders)


# users can create a new hobby
@hobbies_bp.route('/', methods = ['POST'])
@jwt_required()
def create_hobby():
  try:
    # use Marshmallow to load the data
    hobby_info = HobbySchema().load(request.json)
    # assgin the loaded value to the 'name' column of the 'hobbies' table
    hobby = Hobby(
      name = hobby_info['name'].lower(),         
    )
    db.session.add(hobby)
    db.session.commit()

  except IntegrityError:
    return {'error': 'hobby already exists'}, 409

  return HobbySchema().dump(hobby), 201


# admins can edit a hobby
@hobbies_bp.route('/<int:hobby_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(hobby_id):
  admin_required()
  # select the hobby with loaded id then assign new value to it
  stmt = db.select(Hobby).filter_by(id = hobby_id)
  hobby = db.session.scalar(stmt)
  hobby_info = HobbySchema().load(request.json)
  if hobby:
    hobby.name = hobby_info.get('name',hobby.name).lower()
    db.session.commit()
    return HobbySchema().dump(hobby)
  else:
    return {'error': 'hobby_id not found'}, 404
  


# admin can delete a hobby and related user_has_hobby
@hobbies_bp.route('/<int:hobby_id>', methods=['DELETE'])
@jwt_required()
def delect_card(hobby_id):
  admin_required()
  # select the hobby with loaded id then delete it
  stmt = db.select(Hobby).filter_by(id = hobby_id)
  hobby = db.session.scalar(stmt)
  if hobby:
    db.session.delete(hobby)
    db.session.commit()
    return {'message':'Hobby deleted'}, 200
  else:
    return {'error': 'hobby_id not found'}, 404