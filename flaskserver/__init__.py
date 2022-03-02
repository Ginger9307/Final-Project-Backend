from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_socketio import SocketIO, send



app = Flask(__name__)
# Socket server & cors
socketIO = SocketIO(app, cors_allowed_origins='*')
app.config['SOCKET_KEY'] = 'ioKey'
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from flaskserver import routes