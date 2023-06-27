from flask import Blueprint, request
from models.gender import Gender, GenderSchema
from models.user import User, UserSchema
from init import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required,admin_or_owner_required

genders_bp = Blueprint('genders',__name__, url_prefix = '/genders')

# users can view all gender information
@genders_bp.route('/')
@jwt_required()
def all_genders():
   stmt = db.select(Gender)
   genders = db.session.scalars(stmt)
   return GenderSchema(many = True).dump(genders)


# users can create a new gender
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


# users can edit their gender
@genders_bp.route('/my_gender/', methods=['PUT', 'PATCH'])
@jwt_required()
def change_gender():
  stmt = db.select(User).filter_by(id = get_jwt_identity())
  user = db.session.scalar(stmt)
  try:
    user.gender_id = request.json.get('gender_id')
    db.session.commit()
    return UserSchema().dump(user)
  except IntegrityError:
    return {'error': 'Gender_id not exist'}, 400


# admin can edit a gender's name
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