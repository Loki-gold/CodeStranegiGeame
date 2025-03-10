from World import World
from Unit import Unit

from  Manipulator import start_game, start_game2
import asyncio

world = World(10)

u1 = Unit()
u2 = Unit()

world.add_unit(u1,3,3)

world.add_unit(u2,5,5)

async def main():
    await asyncio.gather(start_game(u2), start_game2(u1))

asyncio.run(main())





