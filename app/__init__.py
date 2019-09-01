from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
socketio = SocketIO(app)

from app import routes, models
from app.websockets import (
      handle_client_connect_event,
)


if __name__ == '__main__':
    socketio.run(app)

