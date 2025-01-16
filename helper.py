import json
import datetime
import websocket
import asyncio
from time import sleep


def tojson(dict):
    return json.dumps(dict, indent=2)


# ob = "Storage" action = "Finished"
def log(obj, action, qty, mat, item, *to):
    message = " "
    time = datetime.datetime.now().replace(microsecond=0)
    if obj.__class__.__name__ == "Storage" and action == "finished":  # FINISHED PRODUCTION
        payload = {
            "message": f"[{time}] - Finished production",
            "finished": "true"
        }
        asyncio.create_task(send_websocket_update(tojson(payload)))
        sleep(0.5)
        obj.stop_event.set()  # Set event to indicate completion
    else:
        receiver = obj.__class__.__name__
        message = message.join([f"[{time}] -", receiver, action, str(qty), mat, item])
        payload = {
            "message": message,
            "obj": receiver if receiver else obj,
            "action": action,
            "qty": qty,
            "mat": mat,
            "item": item
        }
        asyncio.create_task(send_websocket_update(tojson(payload)))


async def send_websocket_update(message):
    await websocket.data_send(tojson(message))
    # async with websockets.connect(WEBSOCKET_SERVER) as websocket:
    #     await websocket.serve(message)
    #     print(message)
