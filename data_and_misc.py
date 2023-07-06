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

    def damage(self):
        return self.power + self.bonus_dmg


class Enemy(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.mob_class = ""
        self.type = ""

    unholy = ("Vampire", "Dark Troll")
    undead = ("Zombie", "Necromancer")
    creature = ("Werewolf", "Mad Tree")


# Game variables
class Gv:
    player = Player("", 0, 0)
    enemy = Enemy("", 0, 0)

    run_ans = "yes"
    ans_list = ("yes", "no")
    move_list = ["attack", "run"]

    diff_lvl = 1
    monster_killed = 0

    inventory_dict = {}
    equipped = []

    skill_list = []
    skill_used = "no"

    enemy_sat = 0

    fury_cd = 0


def inventory_print():
    print("Your inventory:")

    if any(Gv.inventory_dict.values()):
        for key, value in Gv.inventory_dict.items():
            if value > 0:
                print(f"{format_items(key)} : {value}")
    else:
        print("Empty")


def answer_check(answer_list, question):
    while (answer := input(f"{question}:\n")) not in answer_list:
        print(f"I don't understand !\n")
    return answer


def format_ans_lists(ans):
    return f"\033[92m{', '.join(ans)}\033[0m"


def format_stats(ans):
    return f"\033[36m{ans}\033[0m"


def format_stats_name(ans):
    return f"\033[34m{ans}\033[0m"


def format_enemy_name(ans):
    return f"\033[31m{ans}\033[0m"


def format_items(ans):
    return f"\033[92m{ans}\033[0m"


def f_back():
    return f"\033[92m back\033[0m"
