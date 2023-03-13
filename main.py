from flask import (
    Flask,
    request,
    session
)
from flask_cors import CORS
from flask_socketio import (
    SocketIO,
    send,
    join_room,
    leave_room
)
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "sfasfasf"
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", 5000, debug=True)
