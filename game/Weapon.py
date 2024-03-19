from Item import Item
from Damage import Damage
from Transform import Transform

class Weapon(Item, Damage):
    def __init__(self, name: str, level: int = 0, value: int = 0,
                 transform: Transform = Transform(0, 0),
                 slash: int = 0, pierce: int = 0, blunt: int = 0,
                 fire: int = 0, ice: int = 0, poison: int = 0, electric: int = 0) -> None:
        Item.__init__(self, name, level, value, transform)
        Damage.__init__(self, slash, pierce, blunt, fire, ice, poison, electric)

        self._damage = Damage(slash, pierce, blunt, fire, ice, poison, electric)

    @property
    def damage(self):
        return self._damage

    @property
    def level(self):
        return self._level

    # Информация о оружии
    def getInfo(self):
        return super().getInfo(), self._damage

class Armor(Item, Damage):
    def __init__(self, name: str, level: int = 0, value: int = 0,
                 transform: Transform = Transform(0, 0),
                 slash: int = 0, pierce: int = 0, blunt: int = 0,
                 fire: int = 0, ice: int = 0, poison: int = 0, electric: int = 0) -> None:
        Item.__init__(self, name, level, value, transform)
        Damage.__init__(self, slash, pierce, blunt, fire, ice, poison, electric)

        self._defence = Damage(slash, pierce, blunt, fire, ice, poison, electric)

    @property
    def defence(self):
        return self._defence

    @property
    def level(self):
        return self._level

    # Информация о оружии
    def getInfo(self):
        return super().getInfo(), self._defence

class Equip(Weapon, Armor):
    



