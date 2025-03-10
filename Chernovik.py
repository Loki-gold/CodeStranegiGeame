import random
import asyncio

class World:
    def __init__(self, world_size):
        self.world_size = world_size
        # Генерируем карту (двумерный массив) со случайными значениями:
        # 1 – лес, 2 – равнина, 3 – горы (пример).
        self.world_status = [
            [random.randint(1, 3) for _ in range(world_size)]
            for _ in range(world_size)
        ]

        # Словарь для хранения позиций юнитов: {(x, y): [unit1, unit2, ...]}
        self.units = {}

    def add_unit(self, unit, x, y):
        """
        Размещаем юнита в мире по координатам (x, y).
        """
        if 0 <= x < self.world_size and 0 <= y < self.world_size:
            if (x, y) not in self.units:
                self.units[(x, y)] = []
            self.units[(x, y)].append(unit)
            unit.world = self
            unit.x, unit.y = x, y  # Сохраняем координаты в объекте юнита
        else:
            raise ValueError("Невозможно разместить юнита за пределами карты!")

    def move_unit(self, unit, dx, dy):
        """
        Перемещаем юнита на dx, dy клеток, если это не выходит за границы карты.
        """
        new_x = unit.x + dx
        new_y = unit.y + dy

        if 0 <= new_x < self.world_size and 0 <= new_y < self.world_size:
            # Убираем юнита с текущей клетки
            if (unit.x, unit.y) in self.units:
                self.units[(unit.x, unit.y)].remove(unit)
                if not self.units[(unit.x, unit.y)]:  # Если клетка опустела, удаляем ключ
                    del self.units[(unit.x, unit.y)]

            # Добавляем юнита на новую клетку
            if (new_x, new_y) not in self.units:
                self.units[(new_x, new_y)] = []
            self.units[(new_x, new_y)].append(unit)

            # Обновляем координаты юнита
            unit.x, unit.y = new_x, new_y
            return True
        return False

    def get_units_at(self, x, y):
        """
        Возвращает список юнитов на клетке (x, y), либо пустой список.
        """
        return self.units.get((x, y), [])

    def __repr__(self):
        return f"<World size={self.world_size} units={len(self.units)}>"

class Unit:
    def __init__(self):
        self.un_id = random.randint(1000000, 9999999)  # уникальный ID
        self.atack_time = 1   # Время атаки (сек)
        self.atack_damage = 1  # Урон за 1 атаку
        self.speed_time = 1   # Время перемещения (сек)
        self.view_range = 3   # Радиус обзора (3 => 7x7)
        self.heal_power = 1   # Сила лечения
        self.heal_time = 1    # Время лечения (сек)
        self.max_hp = 10      # Максимальный HP
        self.hp = self.max_hp  # Текущий HP

        self.now_free = True   # Флаг доступности юнита
        self.world = None      # Ссылка на мир
        self.x, self.y = 0, 0  # Координаты юнита (задаются при размещении)

    async def step(self, dx, dy):
        """
        Двигаем юнита в указанном направлении (dx, dy).
        """
        if self.now_free and self.world:
            self.now_free = False
            await asyncio.sleep(self.speed_time)
            success = self.world.move_unit(self, dx, dy)
            self.now_free = True
            return success
        return False

    def get_vision_map(self):
        """
        Возвращает двумерный массив (7x7 при view_range=3) вокруг юнита.
        Каждый элемент — кортеж (тип локации, список юнитов).
        """
        if not self.world:
            return []

        size = 2 * self.view_range + 1  # Размер квадрата (7 при view_range=3)
        vision_map = []

        for row_offset in range(-self.view_range, self.view_range + 1):
            row_data = []
            for col_offset in range(-self.view_range, self.view_range + 1):
                real_x = self.x + col_offset
                real_y = self.y + row_offset

                if 0 <= real_x < self.world.world_size and 0 <= real_y < self.world.world_size:
                    terrain_type = self.world.world_status[real_y][real_x]
                    units_here = self.world.get_units_at(real_x, real_y)
                    row_data.append((terrain_type, units_here))
                else:
                    row_data.append(None)  # За границами мира
            vision_map.append(row_data)

        return vision_map

    def __repr__(self):
        return f"<Unit id={self.un_id} hp={self.hp}/{self.max_hp} ({self.x}, {self.y})>"

# Тестирование
async def main():
    w = World(10)  # Создаём мир 10x10
    u1 = Unit()
    u2 = Unit()
    u3 = Unit()

    # Размещаем юнитов
    w.add_unit(u1, 5, 5)
    w.add_unit(u2, 6, 5)  # Рядом с u1
    w.add_unit(u3, 7, 5)  # Рядом с u1

    print("World:", w)
    print("u1:", u1)
    print("u2:", u2)
    print("u3:", u3)

    # Посмотрим, что видит u1
    vision = u1.get_vision_map()
    print("\n👀 u1 vision map (7x7):")
    for row in vision:
        print([cell if cell is not None else "X" for cell in row])

    # Двигаем u1 вправо
    await u1.step(1, 0)
    print("\n📍 u1 moved right!")
    print("u1 position:", (u1.x, u1.y))

    # Смотрим карту после перемещения
    vision = u1.get_vision_map()
    print("\n👀 u1 vision map after moving:")
    for row in vision:
        print([cell if cell is not None else "X" for cell in row])

asyncio.run(main())
