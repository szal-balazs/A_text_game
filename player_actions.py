from textgame import *

def player_attack():
    enemy.hp = enemy.hp - player.enemy_damage
    print(f"\nYou attacked.")
    print(f"You dealt {player.enemy_damage} damage.")
    if not e_dead():
        print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
    else:
        print(f"{format_enemy_name(enemy.name)} has no hp left.\n")


def skill_fury():
    if player.fury_cd == 0:
        enemy_hp_before = [enemy.hp]
        enemy.hp = enemy.hp - player.enemy_damage - player.enemy_damage
        player.skill_used = "yes"
        enemy_hp_after = [enemy.hp]
        fury_dmg = enemy_hp_before[0] - enemy_hp_after[0]
        print(f"\nYou used Fury.")
        print(f"You dealt {fury_dmg} damage.")
        if not e_dead():
            print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(enemy.name)} has no hp left.\n")
    elif player.fury_cd > 0:
        print(f"\nYou can't use this skill for {player.fury_cd} turn(s).\n")
    player.fury_cd = 3


def name_create():
    player.name = input("What is your name?\n")
    if len(player.name) == 0:
        player.name = "Anon"
    print(f"Your name is {format_stats(player.name)}.\n")


def player_create():
    player.hp = 20
    player.power = 3


def player_stat():
    stat = {
        "Name": player.name,
        "HP": player.hp,
        "Power": player.power,
        "Damage": player.enemy_damage
    }

    print(f"\nYour stats are:")
    for key in stat.keys():
        print(f"{format_stats_name(key)} : {format_stats(stat[key])}")
