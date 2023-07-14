from game_elements import *


class Character:
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.power = 0

    def dead(self):
        return self.hp <= 0


class Player(Character):

    def __init__(self):
        super().__init__()
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
        name = "Fury"
        if self.fury_cd == 0:
            enemy_hp_before = [enemy.hp]
            enemy.hp = enemy.hp - self.damage() - self.damage()
            enemy_hp_after = [enemy.hp]
            fury_dmg = enemy_hp_before[0] - enemy_hp_after[0]
            print(f"\nYou used {format_skills(name)}.")
            print(f"You dealt {fury_dmg} damage.")
            enemy.hp_left()
            self.skill_used = True
            self.fury_cd = 3

    def turn_end_cooldown(self):
        if self.fury_cd > 0:
            self.fury_cd -= 1

    def reset_cooldown(self):
        self.fury_cd = 0

    def hp_left(self):
        if self.dead():
            print(f"You have no hp left.\n")
        else:
            print(f"Your hp is {format_stats(self.hp)}.\n")

    def can_use_skill(self):
        cooldowns = {
            "Fury" : self.fury_cd
        }

        print(f"Your cooldowns:")
        for key, value in cooldowns.items():
            print(f"{format_skills(key)}: {value}")
        if all(value > 0 for value in cooldowns.values()):
            print(f"You can't use any skills.\n")
            return False
        else:
            return True
