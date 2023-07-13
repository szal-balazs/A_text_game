from game_elements import *


class Character:
    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.power = power

    def dead(self):
        return self.hp <= 0


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
        self.moves = ["attack", "run"]

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

    def create_name(self):
        self.name = input("What is your name?\n")
        if len(self.name) == 0:
            self.name = "Anon"
        print(f"Your name is {format_stats(self.name)}.\n")

    def create_stats(self):
        self.hp = 20
        self.power = 3

    def damage(self):
        return self.power + self.bonus_dmg

    def melee_attack(self, enemy):
        enemy.hp = enemy.hp - self.damage()
        print(f"\nYou attacked.")
        print(f"You dealt {self.damage()} damage.")
        enemy.hp_left()

    def fury(self, enemy):
        if self.fury_cd == 0:
            enemy_hp_before = [enemy.hp]
            enemy.hp = enemy.hp - self.damage() - self.damage()
            self.skill_used = True
            enemy_hp_after = [enemy.hp]
            fury_dmg = enemy_hp_before[0] - enemy_hp_after[0]
            print(f"\nYou used Fury.")
            print(f"You dealt {fury_dmg} damage.")
            enemy.hp_left()
            self.fury_cd = 3
        elif self.fury_cd > 0:
            print(f"\nYou can't use this skill for {self.fury_cd} turn(s).\n")


    def cooldown(self):
        if self.fury_cd > 0:
            self.fury_cd -= 1
        self.skill_used = False

    def hp_left(self):
        if self.dead():
            print(f"You have no hp left.\n")
        else:
            print(f"Your hp is {format_stats(self.hp)}.\n")
