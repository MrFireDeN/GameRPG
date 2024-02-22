class Transform:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def x(self, y: int) -> None:
        self._y = y

    def distance(self, other: 'Transform') -> float:
        return abs(self._x - other._x) + abs(self._y - other._y)

    def __add__(self, other: 'Transform') -> 'Transform':
        return Transform(self._x + other._x, self._y + other._y)

    def __sub__(self, other: 'Transform') -> 'Transform':
        return Transform(self._x - other._x, self._y - other._y)

    def __iadd__(self, other: 'Transform') -> 'Transform':
        self._x += other._x
        self._y += other._y
        return self

    def __isub__(self, other: 'Transform') -> 'Transform':
        self._x -= other._x
        self._y -= other._y
        return self