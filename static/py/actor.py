import inventory, equipment

"""
В лабораторной работе должно быть реализовано:
* конструктор по умолчанию,
* конструктор с параметрами,
* конструктор копирования,
* динамические методы,
* статические методы,
* перегрузка операции,
* работа с уровнями доступа.
"""

class Actor:
    # Поля персонажа

    # Скорость персонажа
    speed = 1
    # Броня персонажа
    armor = 0

    # Иницилизация
    def __init__(self, name: str = 'null_name', level: int = 0, isAlive: bool = true):
        # Имя персонажа
        self.name = name
        # Уровень персонажа
        self.level = level
        # Здоровье персонажа
        self.health = 100 + level*10
        # Жив ли персонаж
        self.isAlive = isAlive
        # Инвентарь
        self.items = inventory.Inventory()
        # Снаряжение
        self.equip = equipment.Equipment()

    def copy(self) -> 'Actor':
        """
        Конструктор копирования.
        """
        new_actor = self.__class__()
        new_actor.__dict__ = self.__dict__
        return actor

    # Жив ли персонаж
    def isAlive(self):
        return self.isAlive
