from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO, send, emit
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__,
      static_url_path='',
      static_folder='static/')

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
socketio = SocketIO(app)
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

from app import routes, models
from app.websockets import (
      handle_client_connect_event,
)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

