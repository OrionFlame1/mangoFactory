import asyncio
from mango import Agent, create_tcp_container, activate
from helper import log

TARGET_PIPES = 10  # Target number of iron pipes to store

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
            parcel = Parcel(10, "Smelter", "mined", "Iron", "Ore")
            log(self, parcel.message, parcel.quantity, parcel.material_type, parcel.item)

            try:
                if parcel.validate("Miner", parcel.receiver):
                    await self.send_message(parcel, smelter.addr)
                    print(f"Miner sent parcel: {parcel}")
                    self.iron_ore -= 10
            except ValueError as e:
                print(f"Parcel validation failed: {e}")
            finally:
                await asyncio.sleep(5)

    def on_ready(self):
        asyncio.create_task(self.mining())


class Smelter(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ore = 0
        self.copper_ore = 0

    def handle_message(self, content, meta):
        if isinstance(content, Parcel):
            log(self, "received", content.quantity, content.material_type, content.item)
            self.iron_ore += content.quantity
            if self.iron_ore >= 10:

                asyncio.create_task(self.smelting())

    async def smelting(self):
        if self.iron_ore >= 20:
            print(f"Smelter is smelting 20 iron ores into 5 iron ingots...")
            await asyncio.sleep(5)
            self.iron_ore -= 20
            parcel = Parcel(5, "Factory", "smelted", "Iron", "Ingots")
            try:
                if parcel.validate("Smelter", parcel.receiver):
                    log(self, parcel.message, parcel.quantity, parcel.material_type, parcel.item)
                    await self.send_message(parcel, factory.addr)
                    print(f"Smelter sent parcel: {parcel}")
            except ValueError as e:
                print(f"Parcel validation failed: {e}")
            finally:
                await asyncio.sleep(5)

            await self.send_message(parcel, factory.addr)
            print(f"Smelter sent 5 iron ingots to Factory.")



class Factory(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ingots = 0
        self.copper_ingots = 0

    def handle_message(self, content, meta):
        if isinstance(content, Parcel):
            self.iron_ingots += content.quantity
            log(self, "received", content.quantity, content.material_type, content.item)
            if self.iron_ingots >= 10:
                asyncio.create_task(self.craft_pipes())

    async def craft_pipes(self):
        print(f"Factory is crafting 5 iron pipes...")
        await asyncio.sleep(5)
        self.iron_ingots -= 10
        quantity = 5
        parcel = Parcel(quantity, storage, "crafted", "Iron", "Pipes")
        log(self, parcel.message, parcel.quantity, parcel.material_type, parcel.item)
        await self.send_message(parcel, storage.addr)
        print(f"Factory sent parcel: {parcel}")
        await asyncio.sleep(5)




class Storage(Agent):
    def __init__(self):
        super().__init__()
        self.iron_pipes = 0
        self.stop_event = asyncio.Event()

    def handle_message(self, content, meta):
        if isinstance(content, Parcel):
            log(self, "received", content.quantity, content.material_type, content.item)
            self.iron_pipes += content.quantity
            if self.iron_pipes >= TARGET_PIPES:
                log(self, "finished", 0, "-", "-")
                self.stop_event.set()  # Set event to indicate completion


async def main():
    container = create_tcp_container(addr=('127.0.0.1', 5555))
    global smelter, factory, storage, miner
    miner = container.register(Miner())
    smelter = container.register(Smelter())
    factory = container.register(Factory())
    storage = container.register(Storage())

    async with activate(container):
        await storage.stop_event.wait()

asyncio.run(main())
