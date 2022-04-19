from flask import jsonify, request
import sys
sys.path.append("..")
from connection import open_config, connection_url

config = open_config()
config = config['postgresql']
schemadb = config['schema']
db = connection_url()

class Users(db.Model):
  __table_args__ = {"schema": schemadb}
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String)

  def __init__(self, name, address):
    self.name = name
    self.address = address

def users_orm():
    if request.method == 'GET':
        users = Users.query.all()
        result = [
            {
                "name": user.name,
                "address": user.address
            } for user in users]
        return jsonify(result)
    
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_users = Users(name=data['name'], address=data['address'])
            db.session.add(new_users)
            db.session.commit()
            return {"message": f"User {new_users.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

def handle_user(user_id):
    user = Users.query.get_or_404(user_id)

    if request.method == 'GET':
        response = {
            "name": user.name,
            "address": user.address
        }
        return {"message": "success", "user": response}

    elif request.method == 'PUT':
        data = request.get_json()
        user.name = data['name']
        user.address = data['address']
        db.session.add(user)
        db.session.commit()
        return {"message": f"user {user.name} successfully updated."}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"message": f"user {user.name} successfully deleted."}

