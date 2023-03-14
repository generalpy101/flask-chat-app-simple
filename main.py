from flask import (
    Flask,
    request,
    session,
    render_template,
    redirect,
    url_for
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
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not username:
            return render_template("index.html", error="Please enter a name", code=code, username=username)

        if join != False and not code:
            return render_template("index.html", error="Please enter a room code", code=code, username=username)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("index.html", error="Room does not exist", code=code, username=username)

        session["room"] = room
        session["username"] = username
        return redirect(url_for("room"))

    return render_template("index.html")


@app.route("/room")
def room():
    room = session.get("room")
    # Prevent unauthorised access
    if room is None or session.get("username") is None or room not in rooms:
        return redirect(url_for("root"))
    return render_template("room.html", room=room, messages=rooms[room]["messages"])


@socketio.on("connect")
def on_connect(auth):
    room = session.get("room")
    username = session.get("username")

    if not room or not username:
        return

    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({
        "username": "username",
        "message": "has entered the room",
    }, to=room)
    rooms[room]["members"] += 1
    print(f"{username} joined the room {room}")


@socketio.on("disconnect")
def on_disconnect():
    room = session.get("room")
    username = session.get("username")

    leave_room(room)

    if room in rooms:
        rooms[room]['members'] -= 1
        if rooms[room]['members'] <= 0:
            del rooms[room]

    send({
        "username": username,
        "message": "has left the room",
    }, to=room)


@socketio.on("message")
def on_message(data):
    room = session.get("room")
    if room not in rooms:
        return
    content = {
        "username": session.get("username"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(content)


if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", 5000, debug=True)
