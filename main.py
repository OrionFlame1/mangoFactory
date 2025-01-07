import asyncio
from mango import Agent, create_tcp_container, activate


class Smelter(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ore = 0

    async def receive_iron_ore(self):
        while True:
            self.iron_ore += 10
            print(f"Smelter received 10 iron ores. Total: {self.iron_ore}")
            if self.iron_ore >= 20:
                await self.smelting()
            await asyncio.sleep(5)

    async def smelting(self):
        if self.iron_ore >= 20:
            print("Smelter is smelting 20 iron ores into 5 iron ingots...")
            await asyncio.sleep(5)
            self.iron_ore -= 20
            await self.send_message(5, receiver_addr=factory.addr)
            print("Smelter sent 5 iron ingots to Factory")

    def on_ready(self):
        asyncio.create_task(self.receive_iron_ore())


class Factory(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ingots = 0

    def handle_message(self, content, meta):
        self.iron_ingots += content
        print(f"Factory received {content} iron ingots. Total: {self.iron_ingots}")
        if self.iron_ingots >= 10:
            asyncio.create_task(self.craft_pipes())

    async def craft_pipes(self):
        print("Factory is crafting 5 iron pipes...")
        await asyncio.sleep(5)
        self.iron_ingots -= 10
        print("5 iron pipes have been crafted!")


async def main():
    container = create_tcp_container(addr=('127.0.0.1', 5555))
    global smelter, factory
    smelter = container.register(Smelter())
    factory = container.register(Factory())

    async with activate(container):
        await asyncio.sleep(40)  # Let the simulation run for some time


asyncio.run(main())
