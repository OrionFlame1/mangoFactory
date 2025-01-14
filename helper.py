import json
import datetime
import websocket
import asyncio

def tojson(dict):
    return json.dumps(dict, indent=2)

async def log(obj, action, qty, mat, item, *to):
    DEBUG = True
    message = " "
    time = datetime.datetime.now().replace(microsecond=0)
    receiver = obj.__class__.__name__
    message = message.join([f"[{time}] -", receiver, action, str(qty), mat, item])
    payload = tojson({
            "message" : message,
            "obj" : receiver if receiver else obj,
            "action" : action,
            "qty" : qty,
            "mat" : mat,
            "item" : item
        })
    if not DEBUG:
        print(tojson({"message" : message}))
        await send_websocket_update(tojson({"message" : message}))
    else:
        print(payload)
        await send_websocket_update(payload)

async def send_websocket_update(message):
    print("function entered")
    await websocket.data_send(message)
    # async with websockets.connect(WEBSOCKET_SERVER) as websocket:
    #     await websocket.serve(message)
    #     print(message)

# log(self, "received", self.iron_ore)

if __name__ == "__main__":
    dict = {}
    dict.add({"iron_ore": 0})
    dict.add({"copper_ore": 0})
    print(tojson(dict))
