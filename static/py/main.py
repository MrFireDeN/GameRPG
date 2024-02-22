from Actor import Actor
from Weapon import Weapon
from Item import Item
from Damage import Damage
from Player import Player

def main():
    Petya = Player("Petya", 1)

    sword = Weapon("меч", 1, 100, Damage(fire = 10))

    print(Damage.calculate_damage(sword.damage), sword.level, Petya.getArmor(), Petya.getLevel())

if __name__ == '__main__':
    main()