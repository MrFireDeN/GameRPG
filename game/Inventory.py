from Item import Item

class Inventory:
    __CAPACITY = 10

    def __init__(self, capacity=__CAPACITY):
        self._capacity = capacity
        self._items = []

    def add_item(self, item: Item):
        if len(self._items) < self._capacity:
            self._items.append(item)
            print(f"Добавлен предмет: {item.name}")
        else:
            print("Инвентарь полон.")

    def remove_item(self, item: Item):
        if item in self._items:
            self._items.remove(item)
            print(f"Удален предмет: {item.name}")
        else:
            print("Предмет не найден в инвенторе.")

    def display_inventory(self):
        if self._items:
            print("Инвентарь:")
            for item in self._items:
                print(f"- {item.name}")
        else:
            print("Инвентарь пустой.")