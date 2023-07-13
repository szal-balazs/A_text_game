from encounters import *
from player import Player
from enemy import Enemy


def main():
    name = ""
    hp = 0
    power = 0

    player = Player(name, hp, power)
    enemy1 = Enemy(name, hp, power)

    player.create_name()
    player.create_stats()

    move_list = ["attack", "run"]

    inventory_dict = {}

    while True:

        for num in range(player.diff_lvl):
            if player.dead():
                break
            fighting_round(player, enemy1, "mob", move_list, inventory_dict)
        if not player.dead():
            if player.diff_lvl == 1:
                find_skill(player, move_list)
            fighting_round(player, enemy1, "boss", move_list, inventory_dict)

        if not player.dead():
            next_lvl(player, inventory_dict)
        elif player.dead():
            restart(player, inventory_dict)


if __name__ == "__main__":
    main()
