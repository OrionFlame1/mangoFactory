import asyncio

from mango import Agent


class Smelter(Agent):
    def __init__(self):
        super().__init__()
        self.iron_ore = 0
        self.copper_ore = 0
        self.ores = 0 # irons + coppers

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
            await self.send_message(5, receiver_addr=factory.addr)
            print(f"Smelter sent 5 iron ingots to Factory")

    def on_ready(self):
        asyncio.create_task(self.receive_iron_ore())