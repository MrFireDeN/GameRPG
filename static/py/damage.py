class Damage():
    _damage_type = ('физический', 'магический')

    def __init__(self, damage_type: str = 'физический', amount: int = 0):
        self.__