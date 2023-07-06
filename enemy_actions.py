import random
from data_and_misc import *


def generate_enemy():
    enemy_name_list = ["Zombie", "Werewolf", "Vampire"]
    Gv.enemy.name = random.choice(enemy_name_list)
    Gv.enemy.hp = 10
    Gv.enemy.power = 2
    Gv.enemy.mob_class = "mob"
    Gv.enemy.type = type_def()


def generate_boss():
    enemy_name_list = ["Dark Troll", "Necromancer", "Mad Tree"]
    Gv.enemy.name = random.choice(enemy_name_list)
    Gv.enemy.hp = 13
    Gv.enemy.power = 3
    Gv.enemy.mob_class = "boss"
    Gv.enemy.type = type_def()


def type_def():
    if Gv.enemy.name in Enemy.unholy:
        return "Unholy"
    elif Gv.enemy.name in Enemy.undead:
        return "Undead"
    elif Gv.enemy.name in Enemy.creature:
        return "Creature"


def enemy_stat():
    e_stat = {
        "Name": Gv.enemy.name,
        "HP": Gv.enemy.hp,
        "Power": Gv.enemy.power,
        "Type": Gv.enemy.type
    }

    for key in e_stat.keys():
        print(f"{format_stats_name(key)} : {format_stats(e_stat[key])}")


def enemy_attack():
    print(f"{format_enemy_name(Gv.enemy.name)} is attacked you.")

    # Special pre damage interactions
    if Gv.enemy.name == "Werewolf":
        werewolf_special()

    # Taking damage
    Gv.player.hp = Gv.player.hp - enemy_damage()

    print(f"{Gv.enemy.name} dealt {enemy_damage()} damage to you.")

    # Resetting damage

    if Gv.enemy.name == "Werewolf" and Gv.enemy_sat <= 3:
        Gv.enemy_sat = 0

    # Special after damage interactions
    if Gv.enemy.name == "Vampire":
        vampire_special()

    # Summary
    if not Gv.player.hp > 0:
        print(f"Your hp is {format_stats(Gv.player.hp)}.\n")
    else:
        print(f"You have no hp left.\n")


def enemy_damage():
    if Gv.enemy.name == "Werewolf" and Gv.enemy_sat == 3:
        bonus_dmg = 2
    else:
        bonus_dmg = 0

    return Gv.enemy.power + bonus_dmg


def werewolf_special():
    Gv.enemy_sat += 1
    if Gv.enemy_sat == 3:
        print(f"The {format_enemy_name(Gv.enemy.name)} slashed you with its claws.")


def vampire_special():
    v_heal = round(random.randint(0, enemy_damage()) / 2)
    Gv.enemy.hp += v_heal
    print(f"{Gv.enemy.name} healed {format_stats(v_heal)} hp and has {format_stats(Gv.enemy.hp)} hp.")
