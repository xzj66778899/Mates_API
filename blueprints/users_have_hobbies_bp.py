from flask import Blueprint, request, jsonify
from models.user import User, UserSchema
from models.hobby import Hobby, HobbySchema
from models.gender import Gender
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

# delete a user's hobby (must be owner of admin role)
@users_have_hobbies_bp.route('/<int:user_has_hobby_id>', methods=['DELETE'])
@jwt_required()
def delect_user_has_hobby(user_has_hobby_id):
  stmt = db.select(User_has_hobby).filter_by(id = user_has_hobby_id)
  user_has_hobby = db.session.scalar(stmt)
  if user_has_hobby:
    admin_or_owner_required(user_has_hobby.user_id)
    db.session.delete(user_has_hobby)
    db.session.commit()
    return {"You don't have this hobby anymore"}, 200
  else:
    return {'error': 'Item not found'}, 404
  


# view users'hobbies
@users_have_hobbies_bp.route('/hobby_users/<int:h_id>')
@jwt_required()
def view_hobby_users(h_id):
   hobby_exists = db.session.query(Hobby.query.filter(Hobby.id == h_id).exists()).scalar()
   if not hobby_exists:
      return {"message":'This hobby ID not exist.'}
   
   stmt = db.select(User_has_hobby).filter_by(hobby_id = h_id)
   hobby_users = db.session.execute(stmt).scalars().first()
   if hobby_users is not None:
      hobby_users_all = db.session.execute(stmt).scalars().all()
      return User_has_hobbySchema(many = True, exclude = ['hobby_id']).dump(hobby_users_all)
   else:
      return{"message":'No one has this hobby yet.'}
   


# view gender's hobbies'
@users_have_hobbies_bp.route('/hobby_genders/<int:g_id>')
@jwt_required()
def view_hobby_genders(g_id):
   gender_exists = db.session.query(Gender.query.filter(Gender.id == g_id).exists()).scalar()
   if not gender_exists:
      return {"message":'This gender ID not exist.'}

   stmt = db.select(User).filter_by(gender_id = g_id)
   gender_users = db.session.execute(stmt).scalars().all()

   if gender_users is not None:
      hobbies = []
      for user in gender_users:
         hobby_stmt = db.select(User_has_hobby).filter_by(user_id = user.id)
         gender_user_hobbies = db.session.execute(hobby_stmt).scalars().all()
         for hobby_list in gender_user_hobbies:
             hobbies.append(hobby_list.hobbies.name)
      if hobbies == []:
         return {"message":'This gender has no hobby yet.'}
      return jsonify(list(hobbies))
   else:
      return{"message":'No user has this gender yet.'}
