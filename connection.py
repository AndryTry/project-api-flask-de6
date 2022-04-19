import yaml
import psycopg2
from flask import Flask
from psycopg2.extras import RealDictCursor
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def open_config():
    location = 'config.yaml'
    with open(location) as file:
        config = yaml.safe_load(file)
    return config

def connection():
    config = open_config()
    config = config['postgresql']

    try:
        connection = psycopg2.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        port=config['port']
        )
        cursor = connection.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        raise e

    return connection, cursor

def connection_url():
    config = open_config()
    config = config['postgresql']
    DB_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(config['user'], config['password'], config['host'], config['port'], config['database'])
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    return db