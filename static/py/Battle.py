from Player import Player
from Enemy import Enemy

class Battle():
    def __init__(self, player: Player, enemy: Enemy):
        self.__player = player
        self.__enemy = enemy
        