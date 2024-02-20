# Снаряжение
class Equipment:
    # Свойства
    _armor_types = ('ничего', 'броня 1', 'броня 2', 'броня 3')
    _weapon_types = ('ничего', 'меч 1', 'меч 2', 'меч 3')
    _item_types = ('ничего', 'лечение 1', 'лечение 2', 'лечение 3')

    # Иницилизация
    def __init__(self, armor_type: str = 'ничего', weapon_type: str = 'ничего',
                 item: str = 'ничего'):
        self.armor = armor_type
        self.weapon = weapon_type
        self.item = item

    # Надеть броню
    def setArmor(self, armor):
        if armor in self._armor_types:
            self.weapon = armor
        else:
            print('такого снаряжения не существует')

    # Надеть меч
    def setWeapon(self, weapon):
        if weapon in self._weapon_types:
            self.weapon = weapon
        else:
            print('такого снаряжения не существует')

    # Надеть броню
    def setItem(self, item):
        if item in self._item_types:
            self.item, = item
        else:
            print('такого снаряжения не существует')
