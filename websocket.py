from flask import Flask, render_template
from flask_socketio import SocketIO
import websockets

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")
#
# def broadcast_message(msg):
#     socketio.emit('message', msg)
#
# if __name__ == '__main__':
#     socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)



# facut de submarin


async def data_send(data):
    url = "ws://localhost:8765"
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(data)
            response = await websocket.recv()
            print (f"{response}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except Exception as e:
        print(f"An error occured: {e}")



