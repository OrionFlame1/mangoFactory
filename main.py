import asyncio

from mango import Agent, create_tcp_container, activate
import helper as h

class Parcel:
    def __init__(self, quantity, receiver, message, material_type, item):
        self.quantity = quantity
        self.receiver = receiver
        self.message = message
        self.material_type = material_type
        self.item = item

    def validate(self, sender_type, receiver_type):
        # Check for compatibility of materials between sender and receiver
        if sender_type == "Miner" and receiver_type == "Factory":
            raise ValueError("Miner cannot send materials directly to Factory.")
        if sender_type == "Smelter" and receiver_type == "Miner":
            raise ValueError("Smelter cannot send items back to Miner.")
        return True

    def __str__(self):
        return f"Parcel(Quantity: {self.quantity}, Material: {self.material_type}, Item: {self.item}, Message: {self.message})"


class Miner(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ore = 0
        self.copper_ore = 0

    async def mining(self):
        while True:
            self.iron_ore += 10
            print(f"Miner mined 10 iron ores. Total: {self.iron_ore}")
            h.log(self, "mined", self.iron_ore, "iron", "ores")
            self.send_parcel("Miner", "Iron", "Iron Ore")
            await asyncio.sleep(5)

    def send_parcel(self, receiver, material_type, item, quantity=10):
        # TODO: jsonify instead of harcoding
        # TODO: Add this function for all Classes
        parcel = Parcel(quantity, receiver, "Iron Ore parcel", material_type, item)
        if parcel.validate("Miner", receiver.__class__.__name__):
            self.send_message(parcel, receiver.addr)
            print(f"Miner sent parcel: {parcel}")
        else:
            print(f"Parcel validation failed for Miner to {receiver.__class__.__name__}.")


class Smelter(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ore = 0
        self.copper_ore = 0

    async def receive_iron_ore(self):
        while True:
            self.iron_ore += 10
            print(f"Smelter received 10 iron ores. Total: {self.iron_ore}")
            if self.iron_ore >= 20:
                await self.smelting()
            await asyncio.sleep(5)

    async def smelting(self):
        if self.iron_ore >= 20:
            print(f"Smelter is smelting 20 iron ores into 5 iron ingots...")
            await asyncio.sleep(5)
            self.iron_ore -= 20
            parcel = Parcel(5, factory, "Iron Ingots parcel", "Iron", "Iron Ingots")
            await self.send_message(parcel, factory.addr)
            print(f"Smelter sent 5 iron ingots to Factory.")

    def on_ready(self):
        asyncio.create_task(self.receive_iron_ore())


class Factory(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ingots = 0

    def handle_message(self, content, meta):
        if isinstance(content, Parcel):
            self.iron_ingots += content.quantity
            print(f"Factory received {content.quantity} iron ingots. Total: {self.iron_ingots}")
            if self.iron_ingots >= 10:
                asyncio.create_task(self.craft_pipes())

    async def craft_pipes(self):
        print(f"Factory is crafting 5 iron pipes...")
        await asyncio.sleep(5)
        self.iron_ingots -= 10
        parcel = Parcel(5, storage, "Iron Pipes parcel", "Iron", "Iron Pipes")
        await self.send_message(parcel, storage.addr)
        print(f"5 iron pipes have been crafted!")


class Storage(Agent):
    def __init__(self):
        super().__init__()
        self.iron_pipes = 0

    def handle_message(self, content, meta):
        if isinstance(content, Parcel):
            self.iron_pipes += content.quantity
            print(f"Storage received {content.quantity} {Parcel}. Total: {self.iron_pipes}")


async def main():
    container = create_tcp_container(addr=('127.0.0.1', 5555))
    global smelter, factory, storage, miner
    miner = container.register(Miner())
    smelter = container.register(Smelter())
    factory = container.register(Factory())
    storage = container.register(Storage())

    async with activate(container):
        await asyncio.sleep(40)  # Let the simulation run for some time


asyncio.run(main())
