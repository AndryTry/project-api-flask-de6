from flask import jsonify, request
import sys
sys.path.append("..")
from connection import open_config, connection

config = open_config()
config = config['postgresql']
schemadb = config['schema']
conn, cursor = connection()

def users():
    if request.method == 'GET':
        query = f"""
        SELECT * FROM {schemadb}.users
        """      
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify(result)
    
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        address = data.get('address')
        query = f"""
        INSERT INTO {schemadb}.users (name, address)
        VALUES ('{name}', '{address}')
        """
        cursor.execute(query)
        conn.commit()
        return {"message": f"Users {name} has been created successfully."}