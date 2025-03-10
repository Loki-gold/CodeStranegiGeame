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
        Возвращает список id юнитов на клетке (x, y), либо пустой список.
        """
        return [i.un_id for i in self.units.get((x, y), [])]

    def __repr__(self):
        return f"<World size={self.world_size} units={len(self.units)}>"
