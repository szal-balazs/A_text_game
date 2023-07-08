from encounters import *


def main():
    name = ""
    hp = 0
    power = 0

    player = Player(name, hp, power)
    enemy1 = Enemy(name, hp, power)

    create_name(player)
    create_player(player)

    move_list = ["attack", "run"]

    inventory_dict = {}

    while True:

        for num in range(player.diff_lvl):
            if dead(player):
                break
            fighting_round(player, enemy1, "mob", move_list, inventory_dict)
        if not dead(player):
            if player.diff_lvl == 1:
                find_skill(player, move_list)
            fighting_round(player, enemy1, "boss", move_list, inventory_dict)

        if not dead(player):
            next_lvl(player, inventory_dict)
        elif dead(player):
            restart(player, inventory_dict)


if __name__ == "__main__":
    main()
