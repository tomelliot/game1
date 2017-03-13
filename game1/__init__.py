import os
from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


app = Flask(__name__)
# load secret key from file. Need to specify a secret key so flask can manage client sessions
app.config.from_pyfile('configuration.py')

# app.config['APPLICATION_ROOT'] = "/game1"
# application = DispatcherMiddleware(Flask('dummy_app'), {
#         app.config['APPLICATION_ROOT']: app,
#     })

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
