from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from models.gender import Gender, GenderSchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required

genders_bp = Blueprint('genders',__name__, url_prefix = '/genders')

# view all gender information
@genders_bp.route('/')
@jwt_required()
def all_genders():
   stmt = db.select(Gender)
   genders = db.session.scalars(stmt)
   return GenderSchema(many = True).dump(genders)


# create a new gender
@genders_bp.route('/', methods = ['POST'])
@jwt_required()
def create_gender():
  try:
    gender_info = GenderSchema().load(request.json)
    gender = Gender(
        name = gender_info['name'].lower(),         
    )
    db.session.add(gender)
    db.session.commit() 
  except IntegrityError:
    return {'error': 'gender is already exist, please view and choose gender_id directly'}, 409

  return GenderSchema().dump(gender), 201


# update a gender
@genders_bp.route('/<int:gender_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(gender_id):
  admin_required()
  stmt = db.select(Gender).filter_by(id = gender_id)
  gender = db.session.scalar(stmt)
  gender_info = GenderSchema().load(request.json)
  if gender:
    gender.name = gender_info.get('name',gender.name),
    db.session.commit()
    return GenderSchema().dump(gender)
  else:
    return {'error': 'Gender not found'}, 404