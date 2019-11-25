from flask_socketio import send, emit
from app import socketio


@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))