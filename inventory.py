from game_elements import *


class Usable:
    def __init__(self):
        self.sword = {"Sword": 0}

    def show(self):
        a = self.__dict__
        b = {}
        for value in a.values():
            b.update(value)
        if any(b.values()):
            for key, value in b.items():
                if value > 0:
                    print(f"{format_items(key)} : {value}")
        else:
            print("Empty")


class Inventory(Usable):
    def __init__(self):
        super().__init__()
        self.health_potion = {"Health potion": 0}
        self.golden_apple = {"Golden apple": 0}
        self.holy_grenade = {"Holy grenade": 0}
        self.fire_bomb = {"Fire bomb": 0}
        self.life_bomb = {"Life bomb": 0}

    def show(self):
        a = self.__dict__
        b = {}
        for value in a.values():
            b.update(value)
        if any(b.values()):
            for key, value in b.items():
                if value > 0:
                    print(f"{format_items(key)} : {value}")
        else:
            print("Empty")


inventory = Inventory()
equipped = Usable()

keys = list(inventory.sword.keys())
inventory.sword[keys[0]] += 1

inventory.show()
equipped.show()
