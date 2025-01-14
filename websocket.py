import websockets

url = "ws://localhost:8765"
async def data_send(data):
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(data)
            response = await websocket.recv()
            print (f"{response}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except Exception as e:
        print(f"An error occured: {e}")