import jwt
from flask import jsonify, request
from . import users_orm
from flask_httpauth import HTTPBasicAuth
from  werkzeug.security import generate_password_hash, check_password_hash
import sys
sys.path.append("..")
from connection import app, open_config, connection_url
from datetime import datetime, timedelta
from functools import wraps

config = open_config()
config = config['postgresql']
schemadb = config['schema']
db = connection_url()
app.config['SECRET_KEY'] = 'kliniksphere154!*&Tjs'

class Users(db.Model):
  __table_args__ = {"schema": schemadb}
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String)
  username = db.Column(db.String)
  password = db.Column(db.String)

  def __init__(self, name, address, username, password):
    self.name = name
    self.address = address
    self.username = username
    self.password = password

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query\
                .filter_by(username = data['username'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        return  f(current_user, *args, **kwargs)
  
    return decorated

def login():
    auth = request.get_json()
  
    if not auth or not auth.get('username') or not auth.get('password'):
        return {'message' : 'Login required !!'}
  
    user = Users.query\
        .filter_by(username = auth.get('username'))\
        .first()
  
    if not user:
        return {'message' : 'User does not exist !!'}
  
    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'username': user.username,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
        return {'token' : token}
    return {'message' : 'Wrong Password !!'}