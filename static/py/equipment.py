from Weapon import Weapon
from Armor import Armor
from Item import Item


# Снаряжение
class Equipment:
    # Иницилизация
    def __init__(self):
        self._weapon = None
        self._armor = None
        self._items = []

    def equip_weapon(self, weapon: Weapon):
        print(f'В снаряжение добавлено оружие {weapon.name}')
        self._weapon = weapon

    def equip_armor(self, armor: Armor):
        print(f'В снаряжение добавлена броня {armor.name}')
        self._armor = armor

    def add_item(self, item: Item):
        if len(self._items) < 3:
            print(f'В снаряжение добавлен предмет {item.name}')
            self._items.append(item)

    def use_item(self, item: int):
        if item >= 0 and item < len(self._items):
            self.__remove_item(self._items[item])
        else:
            print('Нет такого предмета')

    def __remove_item(self, item: Item):
        if item in self._items:
            print(f'Был удален предмет {item.name}')
            self._items.remove(item)

    def info(self):
        return self._weapon.name, self._armor.name, [item.name for item in self._items]