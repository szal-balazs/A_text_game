from encounters import *
from player import Player
from enemy import Enemy


def main():

    player = Player()
    enemy1 = Enemy()

    player.create_name()
    player.create_stats()

    inventory_dict = {}

    while True:

        for num in range(player.diff_lvl):
            if player.dead():
                break
            fighting_round(player, enemy1, "mob", inventory_dict)
        if not player.dead():
            if player.diff_lvl == 1:
                find_skill(player)
            fighting_round(player, enemy1, "boss", inventory_dict)

        if not player.dead():
            next_lvl(player, inventory_dict)
        elif player.dead():
            restart(player, inventory_dict)


if __name__ == "__main__":
    main()
