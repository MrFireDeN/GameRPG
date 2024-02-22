class Item:
    def __init__(self,  name: str, level: int = 0, value: int = 0) -> None:
        self._name = name
        self._level = level
        self._value = value

    def getInfo(self):
        print(f'Name: {self._name}\nLevel: {self._level}\nValue: {self._value}')
        return self._name, self._level, self._value