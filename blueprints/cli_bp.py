from flask import Blueprint
from models.user import User
from models.hobby import Hobby
from models.gender import Gender
from models.user_has_hobby import User_has_hobby
from init import db, bcrypt
from datetime import date



cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_db():
  db.drop_all()
  # drop all the tables
  db.create_all()
  print('Tables created successfully')

@cli_bp.cli.command('seed')
def seed_db():
  genders = [
    Gender(name = 'male'),
    Gender(name = 'female'),
    Gender(name = 'intersex')
  ]

  db.session.query(Gender).delete()
  db.session.add_all(genders)
  db.session.commit()

  users = [
    User(
    first_name = 'Admin',
    password = bcrypt.generate_password_hash('888888').decode('utf8'),
    email = '888888@aaa.com',
    is_admin = True
    ),
    User(
    first_name = 'James',
    last_name = 'Bond',
    password = bcrypt.generate_password_hash('123456').decode('utf8'),
    email = '123456@aaa.com',
    gender_id = genders[0].id
    ),
    User(
    first_name = 'Jason',
    last_name = 'Bourne',
    password = bcrypt.generate_password_hash('654321').decode('utf8'),
    email = '654321@aaa.com',
    gender_id = genders[0].id
    ),
    User(
    first_name = 'Alice',
    last_name = 'Abernathy',
    password = bcrypt.generate_password_hash('222222').decode('utf8'),
    email = '222222@aaa.com',
    gender_id = genders[1].id
    ),
    User(
    first_name = 'Morgan',
    last_name = 'Carpenter',
    password = bcrypt.generate_password_hash('333333').decode('utf8'),
    email = '333333@aaa.com',
    gender_id = genders[2].id
    ),
  ]

  db.session.query(User).delete()
  db.session.add_all(users)
  db.session.commit()

  hobbies = [
    Hobby(name = 'basketball'),
    Hobby(name = 'football'),
    Hobby(name = 'tennis'),
    Hobby(name = 'borad game'),
    Hobby(name = 'hiking'),
    Hobby(name = 'cooking'),
  ]

  db.session.query(Hobby).delete()
  db.session.add_all(hobbies)
  db.session.commit()



