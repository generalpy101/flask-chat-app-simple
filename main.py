from flask import (
    Flask,
    request,
    session,
    render_template
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

rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            return code


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        username = request.form.get("username")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not username:
            return render_template("index.html", erorr="Please enter a name", code=code, username=username)

        if join and not code:
            return render_template("index.html", erorr="Please enter a room code", code=code, username=username)

        room = code
        if create:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("index.html", error="Room does not exist", code=code, username=username)

        session["room"] = room
        session["username"] = username

    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", 5000, debug=True)
