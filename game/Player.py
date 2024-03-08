from Persona import Persona
from Transform import Transform

class Player(Persona):
    def __init__(self, name: str = '', level: int = 0, isAlive: bool = True, transform: Transform = Transform(0, 0)):
        super().__init__(name, level, isAlive, transform)