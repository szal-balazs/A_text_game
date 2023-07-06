from data_and_misc import *


def player_attack():
    Gv.enemy.hp = Gv.enemy.hp - Gv.player.damage()
    print(f"\nYou attacked.")
    print(f"You dealt {Gv.player.damage()} damage.")
    if Gv.enemy.hp > 0:
        print(f"{format_enemy_name(Gv.enemy.name)} has {format_stats(Gv.enemy.hp)} hp left.\n")
    else:
        print(f"{format_enemy_name(Gv.enemy.name)} has no hp left.\n")


def skill_fury():
    if Gv.fury_cd == 0:
        enemy_hp_before = [Gv.enemy.hp]
        Gv.enemy.hp = Gv.enemy.hp - Gv.player.damage() - Gv.player.damage()
        Gv.skill_used = "yes"
        enemy_hp_after = [Gv.enemy.hp]
        fury_dmg = enemy_hp_before[0] - enemy_hp_after[0]
        print(f"\nYou used Fury.")
        print(f"You dealt {fury_dmg} damage.")
        if not Gv.enemy.hp > 0:
            print(f"{format_enemy_name(Gv.enemy.name)} has {format_stats(Gv.enemy.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(Gv.enemy.name)} has no hp left.\n")
    elif Gv.fury_cd > 0:
        print(f"\nYou can't use this skill for {Gv.fury_cd} turn(s).\n")
    Gv.fury_cd = 3


def name_create():
    Gv.player.name = input("What is your name?\n")
    if len(Gv.player.name) == 0:
        Gv.player.name = "Anon"
    print(f"Your name is {format_stats(Gv.player.name)}.\n")


def player_create():
    Gv.player.hp = 20
    Gv.player.power = 3


def player_stat():
    stat = {
        "Name": Gv.player.name,
        "HP": Gv.player.hp,
        "Power": Gv.player.power,
        "Damage": Gv.player.damage()
    }

    print(f"\nYour stats are:")
    for key in stat.keys():
        print(f"{format_stats_name(key)} : {format_stats(stat[key])}")
