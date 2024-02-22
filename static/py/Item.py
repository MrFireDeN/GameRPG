from Transform import Transform

class Item:
    def __init__(self,  name: str, level: int = 0, value: int = 0,
                 transfrom: Transform = Transform(0, 0)) -> None:
        self._name = name
        self._level = level
        self._value = value
        self._transfrom = transfrom

    @property
    def name(self) -> str:
        return self._name

    def getInfo(self):
        print(f'Name: {self._name}\nLevel: {self._level}\nValue: {self._value}')
        return self._name, self._level, self._value