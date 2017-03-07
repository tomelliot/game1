from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# best practice is to move config to file and load from disk on start, and remove file from repo to keep secret a secret
config = {'secret': '1z\xff\xcbZ\xe7e\xbbE\xc5\x9f\x07\xee/\xb1\x92\xa4\xd0\x16\xb2>{\xe9\xb2'}

app = Flask(__name__)
app.secret_key = config['secret'] # need to specify a secret key so flask can manage client sessions

# manage user logins
login_manager = LoginManager()
login_manager.init_app(app)

# manage sockets - live updating of board across different screens
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/test.db'
db = SQLAlchemy(app)
