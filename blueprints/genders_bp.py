from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from models.gender import Gender, GenderSchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity


genders_bp = Blueprint('genders',__name__, url_prefix = '/genders')

# view all gender information
@genders_bp.route('/')
def all_genders():
#    admin_required()
   stmt = db.select(Gender)
   genders = db.session.scalars(stmt)
   return GenderSchema(many = True).dump(genders)


# create a new gender
@genders_bp.route('/', methods = ['POST'])
# @jwt_required()
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

