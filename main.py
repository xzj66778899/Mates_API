from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.hobbies_bp import hobbies_bp
from blueprints.users_have_hobbies_bp import users_have_hobbies_bp
from blueprints.genders_bp import genders_bp
from marshmallow.exceptions import ValidationError
def setup():
  app = Flask(__name__)

  app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
  app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

  db.init_app(app)
  ma.init_app(app)
  jwt.init_app(app)
  bcrypt.init_app(app)


  @app.errorhandler(ValidationError)
  def validation_error(err):
      return {'error':err.__dict__['messages']}, 400


  @app.errorhandler(401)
  def unauthorized(err):
      return {'error': str(err)}, 401

  app.register_blueprint(auth_bp)
  app.register_blueprint(users_have_hobbies_bp)
  app.register_blueprint(cli_bp)
  app.register_blueprint(hobbies_bp)
  app.register_blueprint(genders_bp)

  return app

