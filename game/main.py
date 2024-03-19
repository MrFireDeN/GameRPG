from Persona import Persona
from Weapon import Weapon
from Item import Item
from Damage import Damage
from Player import Player
from Armor import Armor
from Enemy import Enemy
from Equipment import Equipment
from Inventory import Inventory
from Battle import Battle

"""
(1) Специализация X (Player <- Persona)
(2) Спецификация X (SmallHealthPotion <- Consumable)
(3) Обобщение X (HealthPotion <- SmallHealthPotion)
(4) Расширение X (Consumable <- Item)
(5) Ограничение X (Enemy <- Persona)
(6) Конструирование X (EnemyGroup <- Enemy)
(7) Варьирование
(8) Комбинирование X (Weapon <- Item, Damage)
"""

def main():
    # Создание игрока и врага
    player = Player("Петя", 2)
    enemy = Enemy("Вася", 1)

    # Предеметы для игрока
    sword = Weapon("меч", 2, 100, slash=10)
    armor = Armor("Armor", 5, 1000, slash=5, fire=5)
    potion = Item("Potion", 2, 50)

    player.equip.equip_weapon(sword)
    player.equip.equip_armor(armor)
    player.equip.add_item(potion)

    # Предметы для врага
    fiery_hand = Weapon("огненный шар", 1, 50, fire=5)
    enemy.equip.equip_weapon(fiery_hand)

    battle = Battle(player, enemy)
    battle.start_battle()


if __name__ == '__main__':
    main()