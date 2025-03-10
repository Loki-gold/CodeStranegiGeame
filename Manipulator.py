import asyncio

from Unit import Unit


async def start_game(unit: Unit):
    unit.speed_time = 0.9
    f1 = (0, 0)
    # Пока результат шага не сигнализирует, что вышли за границы
    while True:
        f1 = (0, 0)
        while f1[1] != "Out of bounds":
            f1 = await unit.step_up()
            print("f1 :", f1)

            vision = unit.get_vision_map()
            print("\n" * 3)
            for row in vision:
                for cell in row:
                    if cell == None:
                        print(end=' ')
                    elif len(cell[1]) > 0:
                        print(0, end='')
                    else:
                        print("x",end='')
                print()
        f1 = (0, 0)
        while f1[1] != "Out of bounds":
            f1 = await unit.step_left()
            print("f1 :", f1)

            vision = unit.get_vision_map()
            print("\n" * 3)
            for row in vision:
                for cell in row:
                    if cell == None:
                        print(end=' ')
                    elif len(cell[1]) > 0:
                        print(0, end='')
                    else:
                        print("x", end='')
                print()
        f1 = (0, 0)
        while f1[1] != "Out of bounds":
            f1 = await unit.step_down()
            print("f1 :", f1)

            vision = unit.get_vision_map()
            print("\n" * 3)
            for row in vision:
                for cell in row:
                    if cell == None:
                        print(end=' ')
                    elif len(cell[1]) > 0:
                        print(0, end='')
                    else:
                        print("x", end='')
                print()
        f1 = (0, 0)
        while f1[1] != "Out of bounds":
            f1 = await unit.step_right()


            vision = unit.get_vision_map()
            print("\n")
            for row in vision:
                for cell in row:
                    if cell == None:
                        print(end=' ')
                    elif len(cell[1]) > 0:
                        print(0, end='')
                    else:
                        print("x", end='')
                print()



async def start_game2(unit: Unit):
    while True:
        unit.get_vision_map()
        for step in [unit.step_up, unit.step_left, unit.step_down, unit.step_right]:
            while (f1 := await step())[1] != "Out of bounds":
                pass



