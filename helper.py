import json
import datetime

time= datetime.datetime.now()
def tojson(dict):
    return json.dumps(dict)

def log(obj, action, qty, mat, item):
    message = f"[{time}] - "
    if isinstance(obj, str):
        return message + obj
    else:
        receiver = obj.__class__.__name__
        return message.join([receiver, action, qty, mat, item])



# log(self, "received", self.iron_ore)

if __name__ == "__main__":
    dict = {}
    dict.add({"iron_ore": 0})
    dict.add({"copper_ore": 0})
    print(tojson(dict))
