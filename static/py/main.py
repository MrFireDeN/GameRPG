from Actor import Actor
from Weapon import Weapon
from Item import Item
from Damage import Damage
from Player import Player
from Armor import Armor
from Equipment import Equipment
from Inventory import Inventory


def main():
    Petya = Player("Petya", 1)

    sword = Weapon("меч", 1, 100, fire = 10)
    armor = Armor("Armor", 5, 1000, slash= 5, fire = 5)
    potion = Item("Potion", 2, 50)

    print(Damage.calculate_damage(sword.damage, sword.level, armor.defence, armor.level))

    equipment = Equipment()

    equipment.equip_weapon(sword)
    equipment.equip_armor(armor)
    equipment.add_item(potion)
    print(equipment.info())
    equipment.use_item(2)
    print(equipment.info())

    inventory = Inventory()
    
    inventory.display_inventory()
    inventory.add_item(potion)
    inventory.display_inventory()
    inventory.add_item(armor)
    inventory.display_inventory()
    inventory.remove_item(potion)
    inventory.display_inventory()


if __name__ == '__main__':
    main()