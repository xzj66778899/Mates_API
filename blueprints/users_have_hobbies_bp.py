from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from models.user_has_hobby import User_has_hobby, User_has_hobbySchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, admin_or_owner_required


users_have_hobbies_bp = Blueprint('users_have_hobbies',__name__, url_prefix = '/users_have_hobbies')


# view all users'hobbies'
@users_have_hobbies_bp.route('/view')
@jwt_required()
def view_users_hobbies():
   admin_required()
   stmt = db.select(User_has_hobby)
   users_have_hobbies = db.session.scalars(stmt)
   return User_has_hobbySchema(many = True).dump(users_have_hobbies)


# create a new "user's hobby"
@users_have_hobbies_bp.route('/have', methods = ['POST'])
@jwt_required()
def has_hobby():
  user_has_hobby_info = User_has_hobbySchema().load(request.json)

  user_has_hobby = User_has_hobby(
      user_id = get_jwt_identity(),
      hobby_id = user_has_hobby_info['hobby_id']
  )
    
  db.session.add(user_has_hobby)
  db.session.commit()

  return User_has_hobbySchema().dump(user_has_hobby), 201

# delete a user's hobby
@users_have_hobbies_bp.route('/<int:user_has_hobby_id>', methods=['DELETE'])
@jwt_required()
def delect_user_has_hobby(user_has_hobby_id):
  stmt = db.select(User_has_hobby).filter_by(id = user_has_hobby_id)
  user_has_hobby = db.session.scalar(stmt)
  if user_has_hobby:
    admin_or_owner_required(user_has_hobby.user_id)
    db.session.delete(user_has_hobby)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'Item not found'}, 404
  
