from flask import jsonify

def say_hello():
    return jsonify({"text": "Hello World!"})