from game_elements import *
from player import Character
import random


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

    def hp_left(self):
        if not self.dead():
            print(f"{format_enemy_name(self.name)} has {format_stats(self.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(self.name)} has no hp left.\n")

    def generate(self, mob_type, diff_lvl):
        enemy_boss_name_list = ["Dark Troll", "Necromancer", "Mad Tree"]
        enemy_mob_name_list = ["Zombie", "Werewolf", "Vampire"]

        if mob_type == "mob":
            self.name = random.choice(enemy_mob_name_list)
            self.hp = 9 + diff_lvl
            self.power = 2 + random.randint(0, diff_lvl)
        elif mob_type == "boss":
            self.name = random.choice(enemy_boss_name_list)
            self.hp = 11 + 2 * diff_lvl
            self.power = 3 + random.randint(0, diff_lvl)
        self.mob_class = mob_type
        self.type = self.def_type()

    def def_type(self):
        unholy = ("Vampire", "Dark Troll")
        undead = ("Zombie", "Necromancer")
        creature = ("Werewolf", "Mad Tree")

        if self.name in unholy:
            return "Unholy"
        elif self.name in undead:
            return "Undead"
        elif self.name in creature:
            return "Creature"
