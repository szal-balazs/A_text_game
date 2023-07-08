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

    monster_killed = 0
    equipped = []
    skill_list = []
    skill_used = "no"
    fury_cd = 0
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

    enemy_sat = 0

def inventory_print(inventory):
    print("Your inventory:")

    if any(inventory.values()):
        for key, value in inventory.items():
            if value > 0:
                print(f"{format_items(key)} : {value}")
    else:
        print("Empty")


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
