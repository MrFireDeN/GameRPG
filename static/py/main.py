from Actor import Actor
from Weapon import Weapon
from Item import Item
from Damage import Damage

def main():

    Petya = Actor("Petya", 1)

    print(Petya.calculateDamage(Petya.getLevel()))

    Petya.giveExperience(1000)
    if not (Petya.takeDamage(100)):
        del(Petya)

    item1 = Item("Weapon", 2, 10)

    sword = Weapon("меч", 1, 100, Damage(fire = 10))
    print(sword.getInfo())

if __name__ == '__main__':
    main()