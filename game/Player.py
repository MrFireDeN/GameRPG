from Persona import Persona
from Transform import Transform

class Player(Persona):
    def __init__(self, name: str = '', level: int = 0, isAlive: bool = True, transform: Transform = Transform(0, 0)):
        super().__init__(name, level, isAlive, transform)

    # Получение урона персонажем
    def takeDamage(self, damage: int):
        self._health -= damage
        print(f'у вашего персонажа осталось {self._health} здоровья')
        return self.__isAlive()