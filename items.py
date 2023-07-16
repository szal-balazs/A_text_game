import random
from game_elements import *


def get_item(item_name, inventory, move_list):
    if "items" not in move_list:
        move_list.append("items")
    inventory.setdefault(item_name, 0)
    inventory[item_name] += 1


def how_many_items(item_name, inventory):
    item_count = range(1, inventory[item_name])
    uses = 0
    while uses not in item_count:
        try:
            uses = int(input("How many do you want to use ?\n"))
        except ValueError:
            print("Please enter a whole number.")
        else:
            if uses > inventory[item_name]:
                print(f"You don't have that many {format_items(item_name)}. ")
            else:
                break

    return uses


def use_health_potion(player, inventory):
    name = "Health potion"
    uses = how_many_items(name, inventory)
    total_heal = 0
    for i in range(uses):
        inventory[name] -= 1
        total_heal += 5
    total_heal = min(total_heal, player.max_hp - player.hp)
    player.hp += total_heal
    print(f"You healed {total_heal} hp. Your hp is {format_stats(player.hp)} now.\n")


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
    uses = how_many_items(name, inventory)
    for i in range(uses):
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

    uses = how_many_items(bomb_name, inventory)
    damage = 0
    for i in range(uses):
        damage += 6 if is_weak() else 3
    enemy.hp -= damage
    print(f"You dealt {damage} damage.")

    enemy.hp_left()

    inventory[bomb_name] -= 1
