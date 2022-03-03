from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_migrate import Migrate
from decouple import config

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
app.config["JWT_SECRET_KEY"] = config("SECRET_KEY") 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


from flaskserver import routes