import random
import asyncio

class Unit:
    def __init__(self):
        self.un_id = random.randint(1000000, 9999999)  # уникальный идентификатор

        self.atack_time = 1      # время на одну атаку (секунд)
        self.atack_damage = 1    # урон за 1 атаку
        self.speed_time = 1      # время передвижения на соседнюю клетку (секунд)
        self.view_range = 3      # радиус обзора (3 => 7x7)
        self.heal_power = 1      # сколько жизней восстанавливает за 1 цикл лечения
        self.heal_time = 1       # время лечения (секунд)
        self.max_hp = 10         # максимальное количество HP
        self.hp = self.max_hp    # текущий HP

        self.now_free = True     # флаг, свободен ли юнит для нового действия
        self.world = None        # ссылка на мир (устанавливается при add_unit в World)

    async def step_up(self):
        """
        Двигаемся на 1 клетку вверх (y - 1).
        Используем asyncio.sleep для имитации задержки движения.
        """
        if self.now_free:
            self.now_free = False
            await asyncio.sleep(self.speed_time)  # имитация времени на движение

            if self.world is not None:
                success = self.world.move_unit(self, 0, -1)
                self.now_free = True
                if success:
                    return True, "Moved up"
                else:
                    return False, "Out of bounds"
            else:
                self.now_free = True
                return False, "No world reference"
        else:
            return False, "Unit is busy"

    async def step_down(self):
        """
        Двигаемся на 1 клетку вниз (y + 1).
        """
        if self.now_free:
            self.now_free = False
            await asyncio.sleep(self.speed_time)

            if self.world is not None:
                success = self.world.move_unit(self, 0, 1)
                self.now_free = True
                if success:
                    return True, "Moved down"
                else:
                    return False, "Out of bounds"
            else:
                self.now_free = True
                return False, "No world reference"
        else:
            return False, "Unit is busy"

    async def step_left(self):
        """
        Двигаемся на 1 клетку влево (x - 1).
        """
        if self.now_free:
            self.now_free = False
            await asyncio.sleep(self.speed_time)

            if self.world is not None:
                success = self.world.move_unit(self, -1, 0)
                self.now_free = True
                if success:
                    return True, "Moved left"
                else:
                    return False, "Out of bounds"
            else:
                self.now_free = True
                return False, "No world reference"
        else:
            return False, "Unit is busy"

    async def step_right(self):
        """
        Двигаемся на 1 клетку вправо (x + 1).
        """
        if self.now_free:
            self.now_free = False
            await asyncio.sleep(self.speed_time)

            if self.world is not None:
                success = self.world.move_unit(self, 1, 0)
                self.now_free = True
                if success:
                    return True, "Moved right"
                else:
                    return False, "Out of bounds"
            else:
                self.now_free = True
                return False, "No world reference"
        else:
            return False, "Unit is busy"

    async def attack(self, other_unit):
        """
        Атака другого юнита: ждём atack_time, отнимаем hp у цели.
        """
        if self.now_free:
            self.now_free = False
            await asyncio.sleep(self.atack_time)

            if other_unit.hp > 0:
                other_unit.hp -= self.atack_damage
                if other_unit.hp < 0:
                    other_unit.hp = 0
                self.now_free = True
                return True, f"Attacked unit {other_unit.un_id}, now its HP={other_unit.hp}"
            else:
                self.now_free = True
                return False, "Target already dead"
        else:
            return False, "Unit is busy"

    async def heal(self, other_unit):
        """
        Лечение другого юнита: ждём heal_time, восстанавливаем ему hp.
        """
        if self.now_free:
            self.now_free = False
            await asyncio.sleep(self.heal_time)

            if other_unit.hp > 0 and other_unit.hp < other_unit.max_hp:
                other_unit.hp += self.heal_power
                if other_unit.hp > other_unit.max_hp:
                    other_unit.hp = other_unit.max_hp
                self.now_free = True
                return True, f"Healed unit {other_unit.un_id}, now its HP={other_unit.hp}"
            else:
                self.now_free = True
                return False, "No need to heal or target is dead"
        else:
            return False, "Unit is busy"

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
        return f"<Unit id={self.un_id} hp={self.hp}/{self.max_hp}>"