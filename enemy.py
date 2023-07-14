from game_elements import *
from player import Character
import random


class Enemy(Character):

    def __init__(self):
        super().__init__()
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
        if self.dead():
            print(f"{format_enemy_name(self.name)} has no hp left.\n")
        else:
            print(f"{format_enemy_name(self.name)} has {format_stats(self.hp)} hp left.\n")

    def generate(self, player, mob_type):
        enemy_boss_name_list = ["Dark Troll", "Necromancer", "Mad Tree"]
        enemy_mob_name_list = ["Zombie", "Werewolf", "Vampire"]
        diff_lvl = player.diff_lvl
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

    def attack(self, player):
        print(f"{format_enemy_name(self.name)} is attacked you.")
        player_hp_before = player.hp

        if self.name == "Werewolf" and self.spec_att_timer == 2:
            print(f"The {format_enemy_name(self.name)} slashed you with its claws.")
            player.hp = player.hp - 2 * self.power
            self.spec_att_timer = 0
        else:
            player.hp = player.hp - self.power
            self.spec_att_timer += 1

        player_hp_after = player.hp
        damage_dealt = player_hp_before - player_hp_after

        print(f"{self.name} dealt {damage_dealt} damage to you.")

        if self.name == "Vampire":
            v_heal = round(random.randint(0, damage_dealt) / 2)
            self.hp += v_heal
            if v_heal > 0:
                print(f"{format_enemy_name(self.name)} healed {format_stats(v_heal)} hp "
                      f"and has {format_stats(self.hp)} hp.")
            else:
                print(f"{format_enemy_name(self.name)} healed no hp.")


        player.hp_left()
