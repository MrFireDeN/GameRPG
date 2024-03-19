from Persona import Persona
from Transform import Transform

class Enemy(Persona):
    def __init__(self, name: str = '', level: int = 0, isAlive: bool = True, transform: Transform = Transform(0, 0)):
        super().__init__(name, level, isAlive, transform)


    # Повышение уровеня (оргранияение)
    def _levelUp(self):
        print(f"Нельзя повысить уровень для {self._name}")

class EnemyGroup(Enemy):
    def __init__(self, name, level, transform, count: int):
        super.__init__(name, level, True, transform)
        if (count < 0):
            count = 0
            self._isAlive = False
        self.__count = count

    def takeDamage(self, damage: int):
        self._health -= damage
        if self._health <= 0:
            self.__count -= 1
            self._health = self.max_health

        if self.__count <= 0:
            print(f'{self._name} умер :(')
            self._isAlive = False
        return self._isAlive