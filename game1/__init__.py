import os
from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
# best practice is to move config to file and load from disk on start, and remove file from repo to keep secret a secret
config = {'secret': '1z\xff\xcbZ\xe7e\xbbE\xc5\x9f\x07\xee/\xb1\x92\xa4\xd0\x16\xb2>{\xe9\xb2'}

app = Flask(__name__)
app.secret_key = config['secret'] # need to specify a secret key so flask can manage client sessions

# manage user logins
login_manager = LoginManager()
login_manager.init_app(app)

# manage sockets - live updating of board across different screens
socketio = SocketIO(app)

db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db')+os.sep
db_path = os.path.join(db_dir, 'game1.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)
# models.py relies on the db instance, so needs
# to be imported after the db is initialised
from game1 import models 
