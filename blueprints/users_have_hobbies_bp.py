from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from models.user_has_hobby import User_has_hobby, User_has_hobbySchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required


users_have_hobbies_bp = Blueprint('users_have_hobbies',__name__, url_prefix = '/users_have_hobbies')


# view all users'hobbies'
@users_have_hobbies_bp.route('/')
def all_users():
  #  admin_required()
   stmt = db.select(User_has_hobby)
   users_have_hobbies = db.session.scalars(stmt)
   return User_has_hobbySchema(many = True).dump(users_have_hobbies)


# create a new "user's hobby"
@users_have_hobbies_bp.route('/<string:hobby_passed_in>', methods = ['POST'])
@jwt_required()
def has_hobby(hobby_passed_in):

  hobby = db.select(Hobby).filter_by(name = (hobby_passed_in).lower())

  if hobby:
    user_has_hobby = User_has_hobby(
                user_id = get_jwt_identity(),
                hobby_id = hobby.id
                )
    
    db.session.add(user_has_hobby)
    db.session.commit()

  else:
    print ('Hobby not exist, please add new hobby first')
    exit()


  return User_has_hobbySchema().dump(user_has_hobby), 201
