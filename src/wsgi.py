from main import socketio, app
import os

if __name__ == "__main__":
    socketio.run(
        app, "0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT") or 5000, debug=True
    )
