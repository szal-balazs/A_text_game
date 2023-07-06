import random
from data_and_misc import *


def get_item(item_name):
    if "items" not in Gv.move_list:
        Gv.move_list.append("items")
    if item_name not in Gv.inventory_dict:
        Gv.inventory_dict[item_name] = 1
    else:
        Gv.inventory_dict[item_name] += 1


def use_health_potion():
    name = "Health potion"
    if Gv.inventory_dict["Health potion"] <= 0:
        print(f"You have no {format_items(name)}")
    else:
        Gv.inventory_dict[name] -= 1
        heal = 5
        heal = min(heal, Gv.player.max_hp - Gv.player.hp)
        Gv.player.hp += heal
        print(f"You healed {heal} hp. Your hp is {format_stats(Gv.player.hp)} now.\n")


def use_sword():
    name = "Sword"
    if "sword" not in Gv.equipped:
        if name not in Gv.inventory_dict:
            print(f"You have no {format_items(name)}")
        else:
            Gv.inventory_dict[name] -= 1
            Gv.player.bonus_dmg += 2
            Gv.equipped.append("Sword")
            print(f"You equipped the sword. You have {format_stats(Gv.player.damage)} damage now.\n")
    else:
        print(f"You already have a {format_items(name)} equipped.\n")


def use_golden_apple():
    name = "Golden apple"
    if Gv.inventory_dict[name] <= 0:
        print(f"You have no {format_items(name)}")
    else:
        Gv.inventory_dict[name] -= 1
        Gv.player.max_hp += 4
        print(f"You maximum hp increased with 4. It is now {format_stats(Gv.player.max_hp)}.\n")


def generate_bomb():
    bomb_names = ("Holy grenade", "Life bomb", "Fire bomb")
    return random.choice(bomb_names)


def use_bomb(bomb_name):
    Gv.inventory_dict[bomb_name] -= 1

    def is_weak():

        conditions = {
            "Holy grenade": "Unholy",
            "Life bomb": "Undead",
            "Fire bomb": "Creature"
        }
        return Gv.enemy.type == conditions.get(bomb_name, False)

    Gv.enemy.hp -= 6 if is_weak() else 3
    print(f"You dealt {6 if is_weak() else 3} damage.")

    if Gv.enemy.hp > 0:
        print(f"{format_enemy_name(Gv.enemy.name)} has {format_stats(Gv.enemy.hp)} hp left.\n")
    else:
        print(f"{format_enemy_name(Gv.enemy.name)} has no hp left.\n")
