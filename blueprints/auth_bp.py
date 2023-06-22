from flask import Blueprint, request, abort
from models.user import User, UserSchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta


auth_bp = Blueprint('auth', __name__)

# view all users information
@auth_bp.route('/users')
def all_users():
   stmt = db.select(User)
   users = db.session.scalars(stmt)
   return UserSchema(many = True, exclude=['password']).dump(users)


@auth_bp.route('/register', methods = ['POST'])
def register():
  try:
    user_info = UserSchema().load(request.json)
    user = User(
      first_name = user_info['first_name'],
      last_name = user_info['last_name'],
      email = user_info['email'],
      phone = user_info['phone'],
      dob = user_info['dob'],
      password = bcrypt.generate_password_hash(user_info['password']).decode('utf8')
    )
    db.session.add(user)
    db.session.commit()

    return UserSchema(exclude = ['password']).dump(user), 201
  # to avoid duplicated email addresses
  except IntegrityError:
    return {'error': 'email address is already in use'}, 409

@auth_bp.route('/login', methods = ['POST'])
def login():
    try:
      stmt = db.select(User).filter_by(email=request.json['email'])
      user = db.session.scalar(stmt)
      if user and bcrypt.check_password_hash(user.password, request.json['password']):
          token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
          return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
      else:
        return {'error': 'invalid email address or password'}, 401 
    except KeyError:
      return {'error': 'Email and password are required'}, 400


def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
      abort(401, description ='You must be an admin')


def admin_or_owner_required(owner_id):
  user_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  if not (user and (user.is_admin or user_id == owner_id)):
    abort(401, description='You must be an admin or the owner')