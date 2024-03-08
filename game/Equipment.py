from Weapon import Weapon
from Armor import Armor
from Item import Item, Consumable


# Снаряжение
class Equipment:
    # Иницилизация
    def __init__(self):
        self._weapon = None
        self._armor = None
        self._consumables = []

    def equip_weapon(self, weapon: Weapon):
        print(f'В снаряжение добавлено оружие {weapon.name}')
        self._weapon = weapon

    def unequip_weapon(self):
        print(f'Оружие было снята')
        self._weapon = None

    def equip_armor(self, armor: Armor):
        print(f'В снаряжение добавлена броня {armor.name}')
        self._armor = armor

    def unequip_armor(self):
        print(f'Броня было снята')
        self._armor = None

    def add_item(self, item: Consumable):
        if len(self._consumables) < 3:
            print(f'В снаряжение добавлен предмет {item.name}')
            self._consumables.append(item)

    def use_item(self, item: int):
        if item >= 0 and item < len(self._consumables):
            self.__remove_item(self._consumables[item])
        else:
            print('Нет такого предмета')

    def __remove_item(self, item: Consumable):
        if item in self._consumables:
            print(f'Был удален предмет {item.name}')
            self._consumables.remove(item)

    def info(self):
        return self._weapon.name, self._armor.name, [item.name for item in self._consumables]

    @property
    def armor(self):
        return self._armor