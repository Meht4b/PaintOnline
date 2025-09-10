from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import event
from sqlalchemy.engine import Engine
import os 
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit, join_room, leave_room

load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = jwt_secret_key

socket = SocketIO(app, cors_allowed_origins="*")


jwt = JWTManager(app)

CORS(app)

db = SQLAlchemy(app)