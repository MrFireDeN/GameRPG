class Item:
    _item_types = ('weapon', 'armor', 'heal', 'garbage')

    def __init__(self, type: str, name: str, level: int = 0):
        self._type = type
        self._name = name
        self._level = level