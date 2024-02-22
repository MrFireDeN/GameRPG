import Inventory, Equipment

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
    _speed = 1
    # Броня персонажа
    _armor = 0


    def create(self):
        print('Стандартный конструктор')
        # Имя персонажа
        self._name = 'A'
        # Уровень персонажа
        self._level = 0
        # Шкала опыта
        self._ep = (self._level + 1) * 100
        # Максимальное здоровье персонажа
        self._max_health = self.calculateMaxHealth(self._level)
        # Здоровье персонажа
        self._health = self._max_health
        # Жив ли персонаж
        self._isAlive = True
        # Инвентарь
        self._items = Inventory.Inventory()
        # Снаряжение
        self._equip = Equipment.Equipment()


    # Иницилизация
    def __init__(self, name: str = '', level: int = 0, isAlive: bool = True):
        print('Параметризированный конструктор')
        # Имя персонажа
        self._name = name
        # Уровень персонажа
        self._level = level
        # Шкала опыта
        self._ep = (level + 1) * 100
        # Максимальное здоровье персонажа
        self._max_health = 100 + level * 10
        # Здоровье персонажа
        self._health = self._max_health
        # Жив ли персонаж
        self._isAlive = isAlive
        # Инвентарь
        self._items = Inventory.Inventory()
        # Снаряжение
        self._equip = Equipment.Equipment()

    # Конструктор копирования
    def copy(self) -> 'Actor':
        new_actor = self.__class__()
        new_actor.__dict__ = self.__dict__
        return new_actor

    # Получение урона персонажем
    def takeDamage(self, damage: int):
        self._health -= damage
        print(f'у {self._name} осталось {self._health} здоровья')
        return self.__isAlive()

    @staticmethod
    def calculateGainedEP(player_level: int, monster_level: int):
        return int (10 * (monster_level / player_level))


    # Дать опыт
    def gainExperience(self, ep: int = 0):
        self._ep -= ep
        self.__levelUp()


    # Повышение уровеня
    def __levelUp(self):
        if (self._ep >= self._level * 100):
            self._level += 1
            self._ep = 0
            self._max_health += 10
            self._health = self._max_health

            print(f"Уровень увеличен! Теперь ваш уровень: {self._level}")


    def getInfo(self):
        print(f'Персонаж: {self._name}')
        print(f'Уровень: {self._level}')
        print(f'Здоровье: {self._health}/{self._max_health}')
        print(f'Броня: {self._armor}')

    # Жив ли персонаж
    def __isAlive(self):
        if self._health <= 0:
            print(f'{self._name} умер :(')
            self._isAlive = False
        return self._isAlive

    # Геттер для уровня
    def getLevel(self):
        return self._level

    # Геттер для здоровья
    def getHealth(self):
        return self._health

    # Геттер для максимального здоровья
    def getMaxHealth(self):
        return self._max_health

    # Геттер для брони
    def getArmor(self):
        return self._armor

    # Деструктор
    def __del__(self):
        print('Выполняется деструктор!')

    def __add__(self, other):
        return self._level + other._level

    def __iadd__(self, other):
        self._level += other._level

        self._max_health = self.calculateMaxHealth(self._level)
        self._health += other._health

        if (self._health > self._max_health):
            self._health = self._max_health

        return self
