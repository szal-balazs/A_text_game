import random
from formats import *


class Character:
    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.power = power


class Player(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.max_hp = 20
        self.luck = 0
        self.max_luck = 8
        self.bonus_dmg = 0
        self.diff_lvl = 1
        self.equipped = []
        self.skill_list = []
        self.monster_killed = 0
        self.skill_used = False
        self.fury_cd = 0

    def __str__(self):
        stat = {
            "Name": self.name,
            "HP": self.hp,
            "Power": self.power
        }
        s = ""
        for key in stat.keys():
            s += f"{format_stats_name(key)} : {format_stats(stat[key])}\n"
        return s

    def damage(self):
        return self.power + self.bonus_dmg


class Enemy(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.mob_class = ""
        self.type = ""
        self.spec_att_timer = 0

    def __str__(self):
        stat = {
            "Name": self.name,
            "HP": self.hp,
            "Power": self.power
        }
        s = ""
        for key in stat.keys():
            s += f"{format_stats_name(key)} : {format_stats(stat[key])}\n"
        return s


def create_name(player):
    player.name = input("What is your name?\n")
    if len(player.name) == 0:
        player.name = "Anon"
    print(f"Your name is {format_stats(player.name)}.\n")


def create_player(player):
    player.hp = 20
    player.power = 3


def generate_enemy(enemy, mob_type, diff_lvl):
    if mob_type == "mob":
        enemy_name_list = ["Zombie", "Werewolf", "Vampire"]
        enemy.name = random.choice(enemy_name_list)
        enemy.hp = 9 + diff_lvl
        enemy.power = 2 + random.randint(0, diff_lvl)
    elif mob_type == "boss":
        enemy_name_list = ["Dark Troll", "Necromancer", "Mad Tree"]
        enemy.name = random.choice(enemy_name_list)
        enemy.hp = 11 + 2 * diff_lvl
        enemy.power = 3 + random.randint(0, diff_lvl)
    enemy.mob_class = mob_type
    enemy.type = def_type(enemy)


def def_type(enemy):
    unholy = ("Vampire", "Dark Troll")
    undead = ("Zombie", "Necromancer")
    creature = ("Werewolf", "Mad Tree")

    if enemy.name in unholy:
        return "Unholy"
    elif enemy.name in undead:
        return "Undead"
    elif enemy.name in creature:
        return "Creature"


def restart(character, inventory):
    answer_list = "yes", "no"
    run_question = f"Do you want to restart ? {format_ans_lists(answer_list)}"
    run_answer = check_ans_bool(run_question)
    if run_answer:
        inventory.clear()
        create_player(character)
    else:
        print("Bye!")
        exit()


def next_lvl(player, inventory):
    answer_list = "yes", "no"
    next_lvl_question = f"Do you want to go to the next level ? {format_ans_lists(answer_list)}"
    next_lvl_ans = check_ans_bool(next_lvl_question)

    if next_lvl_ans:
        player.diff_lvl += 1
        print(f"\nThe difficulty level is {player.diff_lvl}.\n")
    else:
        restart(player, inventory)


def menu():
    pass


def check_answer(answer_list, question):
    while (answer := input(f"{question}:\n")) not in answer_list:
        print(f"I don't understand !\n")
    return answer


def check_ans_bool(question):
    while (answer := input(f"{question}:\n")) not in ("yes", "no"):
        print(f"I don't understand !\n")

    if answer == "yes":
        return True
    else:
        return False


def dead(character):
    return character.hp <= 0
