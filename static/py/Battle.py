from Player import Player
from Enemy import Enemy
from Actor import Actor

class Battle():
    def __init__(self, player: Player, enemy: Enemy):
        self.__player = player
        self.__enemy = enemy
        self.__winner = None

    def start_battle(self):
        print("Битва началась")

        while True:
            self.__player_turn()
            if self.__is_battle_over():
                break

            self.__enemies_turn()
            if self.__is_battle_over():
                break

            self.__display_battle_result()


    # Логика хода игрока: выбор атаки или использование предмета
    def __player_turn(self):
        print("Ход игрока")
        pass

    # Логика хода врага
    def __enemies_turn(self):
        print("Ход врагов")
        pass


    # Проверяем условия окончания боя, например, если у игрока закончилось здоровье или у врагов
    # Если бой окончен, возвращаем True, иначе - False
    def __is_battle_over(self):
        # Проверяем умер ли игрок
        if self.__player.is_alive == False:
            print(f'{self.__player.name} умер')
            self.__winner = False # Игрок проиграл
            return True

        if self.__enemy.is_alive == False:
            print(f'{self.__enemy.name} умер')
            self.__winner = True # Игрок выиграл
            return True

    # Отображаем результат боя, например, сообщение о победе или поражении
    def __display_battle_result(self):
        if self.__winner:
            print(f'{self.__player.name} победил {self.__enemy.name}!')
        else:
            print(f'{self.__player.name} был побежден {self.__enemy.name}')