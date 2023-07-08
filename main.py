from other import Player, Enemy
from encounters import *


def main():
    name = ""
    hp = 0
    power = 0

    player = Player(name, hp, power)
    enemy = Enemy(name, hp, power)

    create_name(player)
    create_player(player)

    move_list = ["attack", "run"]

    inventory_dict = {}
    diff_lvl = 1

    while True:

        for num in range(diff_lvl):
            if dead(player):
                break
            fighting_round(player, enemy, "mob", inventory_dict)
        if not dead(player):
            if diff_lvl == 1:
                find_skill(player, move_list)
            fighting_round(player, enemy, "boss", inventory_dict)

        if not dead(player):
            next_lvl(player, inventory_dict, diff_lvl)
        elif dead(player):
            restart(player, inventory_dict, diff_lvl)


if __name__ == "main":
    main()
