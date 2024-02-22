from Item import Item
from Damage import Damage

class Weapon(Item):
    def __init__(self, name: str, level: int, value: int, damage: Damage):
        super().__init__(name, level, value)

        self._damage = damage

    # Информация о оружии
    def getInfo(self):
        return super().getInfo(), self._damage



