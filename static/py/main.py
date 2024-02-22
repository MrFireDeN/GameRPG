from Actor import Actor
from Weapon import Weapon
from Item import Item
from Damage import Damage
from Player import Player
from Armor import Armor


def main():
    Petya = Player("Petya", 1)

    sword = Weapon("меч", 1, 100, fire = 10)
    armor = Armor("Armor", 5, 1000, slash= 5, fire = 5)

    print(Damage.calculate_damage(sword.damage, sword.level, armor.defence, armor.level))

if __name__ == '__main__':
    main()