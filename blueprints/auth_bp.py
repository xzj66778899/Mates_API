from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.gender import Gender
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from datetime import timedelta
from sqlalchemy import not_
from marshmallow.validate import ValidationError, Regexp

auth_bp = Blueprint('auth', __name__)

# admin can view all users information
@auth_bp.route('/users')
@jwt_required()
def all_users():
   admin_required()
  #  select users except the admin role
   stmt = db.select(User).where(not_(User.first_name == 'Admin'))
   users = db.session.scalars(stmt)
   return UserSchema(many = True, exclude=['password']).dump(users)


@auth_bp.route('/register', methods = ['POST'])
def register():
  
  user_info = UserSchema().load(request.json)
  g_id = user_info['gender_id']
  confirm_gender_exist = Gender.query.filter_by(id = g_id).first()
  e = user_info['email']
  email_taken = User.query.filter_by(email = e).first()

  if email_taken:
    return {'error': 'email address is already in use'}, 409

  if not confirm_gender_exist:
    return {'error': "This gender_id doesn't exist, please view gender and select another."},400

  user = User(
    first_name = user_info['first_name'],
    last_name = user_info['last_name'],
    email = user_info['email'],
    password = bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
    gender_id = user_info['gender_id']
  )
  db.session.add(user)
  db.session.commit()

  return UserSchema(exclude = ['password','gender_id']).dump(user), 201
    
   
# user login to get token
@auth_bp.route('/login', methods = ['POST'])
def login():
    try:
      stmt = db.select(User).filter_by(email=request.json['email'])
      user = db.session.scalar(stmt)
      if user and bcrypt.check_password_hash(user.password, request.json['password']):
          token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
          return {'token': token, 'welcome user': UserSchema(exclude=['password']).dump(user)}
      else:
          return {'error': 'invalid email address or password'}, 401 
    except KeyError:
      return {'error': 'Email and password are required'}, 400


# users can change their own password
@auth_bp.route('/change_password', methods = ['POST'])
@jwt_required()
def change_password():
   user_id = get_jwt_identity()
   stmt = db.select(User).filter_by(id = user_id)
   current_user = db.session.scalar(stmt)

   data = request.get_json()

   old_password = data.get('old_password')
   new_password = data.get('new_password')

   if old_password is None or new_password is None:
        return {"error": "Old and new passwords are required."}, 400
   
   if not bcrypt.check_password_hash(current_user.password, old_password):
        return {"error": "Old password is incorrect."}, 400

   password_validator = Regexp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        error='Password should contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long'
    )

   try:
       password_validator(new_password)
   except ValidationError as err:
       return {"error": err.messages[0]}, 400
   

   current_user.password = bcrypt.generate_password_hash(new_password).decode('utf8')
   db.session.commit()

   return {"message": "Password has been updated successfully."}



# admin authorization
def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
      abort(401, description ='You must be an admin')

# admin or owner authorization 
def admin_or_owner_required(owner_id):
  user_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  if not (user and (user.is_admin or user_id == owner_id)):
    abort(401, description='You must be an admin or the owner')