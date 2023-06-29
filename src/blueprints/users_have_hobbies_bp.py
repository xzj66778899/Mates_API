from flask import Blueprint, request, jsonify
from models.gender import Gender
from models.hobby import Hobby
from models.user import User
from models.user_has_hobby import User_has_hobby, User_has_hobbySchema
from sqlalchemy.exc import IntegrityError
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_or_owner_required


users_have_hobbies_bp = Blueprint('users_have_hobbies',__name__, url_prefix = '/users_have_hobbies')


# users can view all users'hobbies'
@users_have_hobbies_bp.route('/view')
@jwt_required()
def view_users_hobbies():
   # select all rows in users_have_hobbies tables
   stmt = db.select(User_has_hobby)
   users_have_hobbies = db.session.scalars(stmt)
   return User_has_hobbySchema(many = True).dump(users_have_hobbies)


# users can view their own hobbies/
@users_have_hobbies_bp.route('/mine')
@jwt_required()
def view_my_hobbies():
   # select rows in users_have_hobbies tables with loaded user_id
   stmt = db.select(User_has_hobby).filter_by(user_id = get_jwt_identity())
   users_have_hobbies = db.session.scalars(stmt)
   return User_has_hobbySchema(many = True).dump(users_have_hobbies)
   

# users can link them to a new hobby
@users_have_hobbies_bp.route('/have', methods = ['POST'])
@jwt_required()
def has_hobby():
  try:
    # check if the user already has this hobby, also prevent dupulicated row in the database
    user_has_hobby_info = User_has_hobbySchema().load(request.json)

    user_id = get_jwt_identity()
    hobby_id = user_has_hobby_info['hobby_id']
   # select the first item in table that the columns are the same to the loaded data 
    existing_hobby = User_has_hobby.query.filter_by(user_id = user_id, hobby_id = hobby_id).first()

    if existing_hobby:
        return {"error": "You already has this hobby!"}, 400
    
   # add a new row to the table
    user_has_hobby = User_has_hobby(
        user_id = get_jwt_identity(),
        hobby_id = user_has_hobby_info['hobby_id']
    )
      
    db.session.add(user_has_hobby)
    db.session.commit()

    return User_has_hobbySchema(exclude = ["hobby_id"]).dump(user_has_hobby)
  except IntegrityError:
    return {"error":"This hobby_id doesn't exist, please select another one."},400


#admin or owner can delete a user's hobby
@users_have_hobbies_bp.route('/<int:user_has_hobby_id>', methods=['DELETE'])
@jwt_required()
def delete_user_has_hobby(user_has_hobby_id):
  #Select the row with loaded id, if not None, delete the row.
  stmt = db.select(User_has_hobby).filter_by(id = user_has_hobby_id)
  user_has_hobby = db.session.scalar(stmt)
  if user_has_hobby:
    admin_or_owner_required(user_has_hobby.user_id)
    db.session.delete(user_has_hobby)
    db.session.commit()
    return {'message': "You don't have this hobby anymore"}, 200
  else:
    return {'error': 'Item not found'}, 404
  

# users can view all the users who have the particular hobby
@users_have_hobbies_bp.route('/hobby_users/<int:h_id>')
@jwt_required()
def view_hobby_users(h_id):
   # Check if the hobbies table has the loaded hobby_id. The 'exist()' will return a boolean value.
   hobby_exists = db.session.query(Hobby.query.filter(Hobby.id == h_id).exists()).scalar()
   if not hobby_exists:
      return {"error":"This hobby_id doesn't exist."}
   # select items in 'users_have_hobbies' table with hobby_id
   stmt = db.select(User_has_hobby).filter_by(hobby_id = h_id)
   # select the first item to check if its 'None' or not
   hobby_users = db.session.scalars(stmt).first()
   if hobby_users is not None:
      # if it's not None, then choose all of them
      hobby_users_all = db.session.scalars(stmt).all()
      return User_has_hobbySchema(many = True, exclude = ['hobby_id']).dump(hobby_users_all)
   else:
      return{"message":'No one has this hobby yet.'}
   

# users can view all the hobbies that one particluar gender have
@users_have_hobbies_bp.route('/hobby_genders/<int:g_id>')
@jwt_required()
def view_hobby_genders(g_id):
   # check if the loaded gender_id exist in the database
   gender_exists = db.session.query(Gender.query.filter(Gender.id == g_id).exists()).scalar()
   if not gender_exists:
      return {"message":"This gender_id doesn't exist."}
   # select all users with loaded gender_id
   stmt = db.select(User).filter_by(gender_id = g_id)
   gender_users = db.session.scalars(stmt).all()

   if gender_users:
      hobbies = []
      # for every item in gender_users,get the users_have_hobbies item.
      for user in gender_users:
         hobby_stmt = db.select(User_has_hobby).filter_by(user_id = user.id)
         gender_user_hobbies = db.session.scalars(hobby_stmt).all()
         # for every item in users_have_hobbies, get the hobbies_name and gather them in a list
         for hobby_list in gender_user_hobbies:
             hobbies.append(hobby_list.hobbies.name)
      if hobbies == []:
         return {"message":'This gender has no hobby yet.'}
      return jsonify(list(hobbies))
   else:
      return{"message":'No user has this gender yet.'}
