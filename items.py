import random
from game_elements import *


def get_item(item_name, inventory, move_list):
    if "items" not in move_list:
        move_list.append("items")
    inventory.setdefault(item_name, 0)
    inventory[item_name] += 1


def use_health_potion(player, inventory):
    name = "Health potion"
    if inventory[name] <= 0:
        print(f"You have no {format_items(name)}")
    else:
        inventory[name] -= 1
        heal = 5
        heal = min(heal, player.max_hp - player.hp)
        player.hp += heal
        print(f"You healed {heal} hp. Your hp is {format_stats(player.hp)} now.\n")


def use_sword(player, inventory):
    name = "Sword"
    if name not in player.equipped:
        if name not in inventory:
            print(f"You have no {format_items(name)}")
        else:
            inventory[name] -= 1
            player.bonus_dmg += 2
            player.equipped.append(name)
            print(f"You equipped the {format_items(name)}. You deal {format_stats(player.damage())} damage now.\n")
    else:
        print(f"You already have a {format_items(name)} equipped.\n")


def use_golden_apple(player, inventory):
    name = "Golden apple"
    if inventory[name] <= 0:
        print(f"You have no {format_items(name)}")
    else:
        inventory[name] -= 1
        player.max_hp += 4
        print(f"You maximum hp increased with 4. It is now {format_stats(player.max_hp)}.\n")


def generate_bomb():
    bomb_names = ("Holy grenade", "Life bomb", "Fire bomb")
    return random.choice(bomb_names)


def use_bomb(bomb_name, enemy, inventory):
    def is_weak():
        conditions = {
            "Holy grenade": "Unholy",
            "Life bomb": "Undead",
            "Fire bomb": "Creature"
        }
        return enemy.type == conditions.get(bomb_name, False)

    enemy.hp -= 6 if is_weak() else 3
    print(f"You dealt {6 if is_weak() else 3} damage.")

    enemy.hp_left()

    inventory[bomb_name] -= 1
