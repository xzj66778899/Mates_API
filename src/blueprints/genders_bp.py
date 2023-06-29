from flask import Blueprint, request
from models.gender import Gender, GenderSchema
from models.user import User, UserSchema
from init import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required

genders_bp = Blueprint('genders',__name__, url_prefix = '/genders')

# users can view all gender information
@genders_bp.route('/')
def all_genders():
  #  select the Gender Class in Pythion (the genders table in database) 
   stmt = db.select(Gender)
  #  select multiple rows so we use 'scalars' instead of 'scalar'
   genders = db.session.scalars(stmt)
   return GenderSchema(many = True).dump(genders)


# users can create a new gender
@genders_bp.route('/', methods = ['POST'])
@jwt_required()
def create_gender():
  try:
    # get the loaded gender name then add to the 'Gender' Class('genders' table) in database
    gender_info = GenderSchema().load(request.json)
    gender = Gender(
        name = gender_info['name'].lower(),         
    )
    db.session.add(gender)
    db.session.commit() 
  except IntegrityError:
    return {'error': 'gender already exists'}, 409

  return GenderSchema().dump(gender), 201


# users can edit their genders
@genders_bp.route('/my_gender/', methods=['PUT', 'PATCH'])
@jwt_required()
def change_gender():
  # select user that matches the id in the login token
  stmt = db.select(User).filter_by(id = get_jwt_identity())
  user = db.session.scalar(stmt)
  try:
    # assign the gender_id column a new value from loaded data
    user.gender_id = request.json.get('gender_id')
    db.session.commit()
    return UserSchema(exclude=['password']).dump(user)
  except IntegrityError:
    return {'error': 'gender_id not exist'}, 400


# admin can edit a gender
@genders_bp.route('/<int:gender_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(gender_id):
  admin_required()
  # select a gender with loaded id
  stmt = db.select(Gender).filter_by(id = gender_id)
  gender = db.session.scalar(stmt)
  gender_info = GenderSchema().load(request.json)
  if gender:
    # assign the name of the selected gender a new loaded value, or the current value if no data loaded 
    gender.name = gender_info.get('name',gender.name),
    db.session.commit()
    return GenderSchema().dump(gender)
  else:
    return {'error': 'Gender not found'}, 404