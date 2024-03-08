from Transform import Transform
from Actor import Actor
from Damage import Damage

# Класс предметов
class Item:
    def __init__(self,  name: str, level: int = 0, value: int = 0,
                 transfrom: Transform = Transform(0, 0)) -> None:
        self._name = name
        self._level = level
        self._value = value
        self._transfrom = transfrom

    @property
    def name(self) -> str:
        return self._name

    def getInfo(self):
        print(f'Name: {self._name}\nLevel: {self._level}\nValue: {self._value}')
        return self._name, self._level, self._value

# Класс расходников
class Consumable(Item):
    def __init__(self,  name: str, level: int = 0, value: int = 0,
                 transfrom: Transform = Transform(0, 0)) -> None:
        super().__init__(self, name, level, value, transfrom)

    def use(self, target: Actor) -> None:
        pass

# Класс зелья лечения
class HealthPotion(Consumable):
    def __init__(self, level: int = 1, value: int = 50,
                 transfrom: Transform = Transform(0, 0)) -> None:
        super().__init__(self, "Зелье лечения", level, value, transfrom)

    def use(self, target: Actor) -> None:
        target.heal(self._level * 50)
        print(f"{target.name} использует {self._name} {self._level}")


# Класс бомбы
class Bomb(Consumable):
    def __init__(self, name: str = "Бомба", level: int = 1, value: int = 100,
                 transfrom: Transform = Transform(0, 0), damage: Damage = Damage(fire=5)) -> None:
        super().__init__(self, name, level, value, transfrom)
        self._damage = damage

    def use(self, target: Actor) -> None:
        target.takeDamage(Damage.calculate_damage(self._damage, self._level, target.armor.defence, target.armor.level))
        print(f"{self._name} {self._level} взорволась рядом с {target.name}")