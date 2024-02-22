from Actor import Actor

class Player(Actor):
    def __init__(self, name: str = '', level: int = 0, isAlive: bool = True):
        super().__init__(name, level, isAlive)