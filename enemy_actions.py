from textgame import *
import random


def generate_enemy():
    enemy_name_list = ["Zombie", "Werewolf", "Vampire"]
    enemy.name = random.choice(enemy_name_list)
    enemy.hp = 10
    enemy.power = 2
    enemy.mob_class = "mob"
    enemy.type = enemy.type_def()


def generate_boss():
    enemy_name_list = ["Dark Troll", "Necromancer", "Mad Tree"]
    enemy.name = random.choice(enemy_name_list)
    enemy.hp = 13
    enemy.power = 3
    enemy.mob_class = "boss"
    enemy.type = enemy.type_def()


def type_def():
    if enemy.name in Enemy.unholy:
        return "Unholy"
    elif enemy.name in Enemy.undead:
        return "Undead"
    elif enemy.name in Enemy.creature:
        return "Creature"


def enemy_stat():
    e_stat = {
        "Name": enemy.name,
        "HP": enemy.hp,
        "Power": enemy.power,
        "Type": enemy.type
    }

    for key in e_stat.keys():
        print(f"{format_stats_name(key)} : {format_stats(e_stat[key])}")


def enemy_attack():
    print(f"{format_enemy_name(enemy.name)} is attacked you.")

    # Special pre damage interactions
    if enemy.name == "Werewolf":
        enemy.werewolf_special()

    # Taking damage
    player.hp = int(player.hp) - int(enemy.enemy_damage())

    print(f"{enemy.name} dealt {enemy.enemy_damage()} damage to you.")

    # Resetting damage

    if enemy.name == "Werewolf" and Enemy.spec_att_timer <= 3:
        enemy.spec_att_timer = 0

    # Special after damage interactions
    if enemy.name == "Vampire":
        enemy.vampire_special()

    # Summary
    if not p_dead():
        print(f"Your hp is {format_stats(player.hp)}.\n")
    else:
        print(f"You have no hp left.\n")


def enemy_damage():
    if enemy.name == "Werewolf" and Enemy.spec_att_timer == 3:
        bonus_dmg = 2
    else:
        bonus_dmg = 0

    return int(enemy.power) + bonus_dmg


def werewolf_special():
    Enemy.spec_att_timer += 1
    if Enemy.spec_att_timer == 3:
        print(f"The {format_enemy_name(enemy.name)} slashed you with its claws.")


def vampire_special():
    v_heal = round(random.randint(0, int(enemy.enemy_damage())) / 2)
    enemy.hp += v_heal
    print(f"{enemy.name} healed {format_stats(v_heal)} hp and has {format_stats(enemy.hp)} hp.")
