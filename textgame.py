import random
from loot import looting

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

    skill_list = []
    skill_used = "no"

    fury_cd = 0


class Enemy(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.mob_class = ""
        self.type = ""

    spec_att_timer = 0

    unholy = ("Vampire", "Dark Troll")
    undead = ("Zombie", "Necromancer")
    creature = ("Werewolf", "Mad Tree")


class GameVar:
    run_ans = "yes"
    ans_list = ("yes", "no")
    diff_lvl = 1
    monster_killed = 0
    inventory_dict = {}
    equipped = []
    move_list = ["attack", "run"]


# Formats -----------------------------------------------------------
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


def player_attack():
    enemy.hp = enemy.hp - player.damage()
    print(f"\nYou attacked.")
    print(f"You dealt {player.damage()} damage.")
    if not e_dead():
        print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
    else:
        print(f"{format_enemy_name(enemy.name)} has no hp left.\n")


def skill_fury():
    if player.fury_cd == 0:
        enemy_hp_before = [enemy.hp]
        enemy.hp = enemy.hp - player.damage() - player.damage()
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
        "Power": player.power
    }

    print(f"\nYour stats are:")
    for key in stat.keys():
        print(f"{format_stats_name(key)} : {format_stats(stat[key])}")


def inventory_print():
    print("Your inventory:")

    if any(GameVar.inventory_dict.values()):
        for key, value in GameVar.inventory_dict.items():
            if value > 0:
                print(f"{format_items(key)} : {value}")
    else:
        print("Empty")


def generate_enemy():
    enemy_name_list = ["Zombie", "Werewolf", "Vampire"]
    enemy.name = random.choice(enemy_name_list)
    enemy.hp = 10
    enemy.power = 2
    enemy.mob_class = "mob"
    enemy.type = type_def()


def generate_boss():
    enemy_name_list = ["Dark Troll", "Necromancer", "Mad Tree"]
    enemy.name = random.choice(enemy_name_list)
    enemy.hp = 13
    enemy.power = 3
    enemy.mob_class = "boss"
    enemy.type = type_def()


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
        werewolf_special()

    # Taking damage
    player.hp = int(player.hp) - int(enemy_damage())

    print(f"{enemy.name} dealt {enemy_damage()} damage to you.")

    # Resetting damage

    if enemy.name == "Werewolf" and Enemy.spec_att_timer <= 3:
        enemy.spec_att_timer = 0

    # Special after damage interactions
    if enemy.name == "Vampire":
        vampire_special()

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
    v_heal = round(random.randint(0, int(enemy_damage())) / 2)
    enemy.hp += v_heal
    print(f"{enemy.name} healed {format_stats(v_heal)} hp and has {format_stats(enemy.hp)} hp.")


def get_item(item_name):
    if "items" not in GameVar.move_list:
        GameVar.move_list.append("items")
    if item_name not in GameVar.inventory_dict:
        GameVar.inventory_dict[item_name] = 1
    else:
        GameVar.inventory_dict[item_name] += 1


def use_health_potion():
    name = "Health potion"
    if GameVar.inventory_dict["Health potion"] <= 0:
        print(f"You have no {format_items(name)}")
    else:
        GameVar.inventory_dict[name] -= 1
        heal = 5
        heal = min(heal, player.max_hp - player.hp)
        player.hp += heal
        print(f"You healed {heal} hp. Your hp is {format_stats(player.hp)} now.\n")


def use_sword():
    name = "Sword"
    if "sword" not in GameVar.equipped:
        if name not in GameVar.inventory_dict:
            print(f"You have no {format_items(name)}")
        else:
            GameVar.inventory_dict[name] -= 1
            player.bonus_dmg += 2
            GameVar.equipped.append("Sword")
            print(f"You equipped the sword.\n")
    else:
        print(f"You already have a {format_items(name)} equipped.\n")


def use_golden_apple():
    name = "Golden apple"
    if GameVar.inventory_dict[name] <= 0:
        print(f"You have no {format_items(name)}")
    else:
        GameVar.inventory_dict[name] -= 1
        player.max_hp += 4
        print(f"You maximum hp increased with 4. It is now {format_stats(player.max_hp)}.\n")


def generate_bomb():
    bomb_names = ("Holy grenade", "Life bomb", "Fire bomb")
    return random.choice(bomb_names)


def use_bomb(bomb_name):
    GameVar.inventory_dict[bomb_name] -= 1

    def is_weak():

        conditions = {
            "Holy grenade": "Unholy",
            "Life bomb": "Undead",
            "Fire bomb": "Creature"
        }
        return enemy.type == conditions.get(bomb_name, False)

    enemy.hp -= 6 if is_weak() else 3
    print(f"You dealt {6 if is_weak() else 3} damage.")

    if not e_dead():
        print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
    else:
        print(f"{format_enemy_name(enemy.name)} has no hp left.\n")


# Game components -------------------------------------------------------

def answer_check(answer_list, question):
    while (answer := input(f"{question}:\n")) not in answer_list:
        print(f"I don't understand !\n")
    return answer


def fight():
    print(f"You have been attacked by {format_enemy_name(enemy.name)}.")
    enemy_stat()
    skip_list = ["run"]
    fight_question = f"What do you want to do ? {format_ans_lists(GameVar.move_list)}"
    move_ans = answer_check(GameVar.move_list, fight_question)

    def turn_end():
        if player.fury_cd > 0:
            player.fury_cd -= 1
        player.skill_used = "no"

    def fight_death_check():
        if p_dead():
            print(f"You died! Monster(s) killed: {GameVar.monster_killed}\n")
            return True
        elif e_dead():
            print("You win!\n")
            GameVar.monster_killed += 1
            return True

    while move_ans not in skip_list:
        if move_ans == "attack":
            player_attack()
            if not e_dead():
                enemy_attack()
            if fight_death_check():
                skip_list.append("exit")
                move_ans = "exit"
            else:
                move_ans = answer_check(GameVar.move_list, fight_question)

        if "items" in GameVar.move_list:
            if move_ans == "items":
                inventory_print()
                item_use_ans = input(f"\nWhat item do you want to use (or go{f_back()})\n")
                while item_use_ans not in GameVar.inventory_dict.keys() and item_use_ans != "back":
                    inventory_print()
                    item_use_ans = input(f"Try again or go{f_back()})\n")

                if item_use_ans == "Health potion":
                    use_health_potion()
                elif item_use_ans == "Sword":
                    use_sword()
                elif item_use_ans == "Golden apple":
                    use_golden_apple()
                elif item_use_ans in ["Holy grenade", "Life bomb", "Fire bomb"]:
                    use_bomb(item_use_ans)

                if fight_death_check():
                    skip_list.append("exit")
                    move_ans = "exit"
                else:
                    move_ans = answer_check(GameVar.move_list, fight_question)

        if "skills" in GameVar.move_list:
            if move_ans == "skills":
                skill_use_ans = input(f"\nWhat skill do you want to use (or go{f_back()})? "
                                      f"{format_ans_lists(player.skill_list)}:\n")
                while skill_use_ans not in player.skill_list and skill_use_ans != "back":
                    skill_use_ans = input(f"Try again or go{f_back()}."
                                          f"{format_ans_lists(player.skill_list)}\n")
                if skill_use_ans == "Fury":
                    skill_fury()

                if player.skill_used == "yes":
                    if not e_dead():
                        enemy_attack()
                    if fight_death_check():
                        skip_list.append("exit")
                        move_ans = "exit"
                    else:
                        move_ans = answer_check(GameVar.move_list, fight_question)
                else:
                    move_ans = answer_check(GameVar.move_list, fight_question)
        turn_end()

    if move_ans == "run":
        print("You ran away!\n")
    if "exit" in skip_list:
        skip_list.remove("exit")


def skill_find():
    skill_question = f"\nYou found a book. Do you want to learn a new skill ?" \
                     f" {format_ans_lists(GameVar.ans_list)}"
    skill_ans = answer_check(GameVar.ans_list, skill_question)
    if skill_ans == "yes":
        if "skills" not in GameVar.move_list:
            GameVar.move_list.append("skills")
        player.skill_list.append("Fury")
        print("You learned a new skill.")


# Other game elements ------------------------------------
def restart():
    run_question = f"Do you want to restart ? {format_ans_lists(GameVar.ans_list)}"
    GameVar.run_ans = answer_check(GameVar.ans_list, run_question)
    if GameVar.run_ans == "no":
        print("Bye!")
        exit()
    elif GameVar.run_ans == "yes":
        GameVar.diff_lvl = 1
        GameVar.inventory_dict.clear()
        player_create()


def mob_round():
    player_stat()
    generate_enemy()
    fight()
    if not p_dead():
        looting(player.luck, "mob")


def boss_round():
    player_stat()
    generate_boss()
    fight()
    if not p_dead():
        looting(player.luck, "boss")


def next_lvl():
    next_lvl_question = f"Do you want to go to the next level ? {format_ans_lists(GameVar.ans_list)}"
    next_lvl_ans = answer_check(GameVar.ans_list, next_lvl_question)

    if next_lvl_ans == "no":
        restart()
    elif next_lvl_ans == "yes":
        GameVar.diff_lvl += 1
        print(f"\nThe difficulty level is {GameVar.diff_lvl}.\n")


def p_dead():
    return player.hp <= 0


def e_dead():
    return enemy.hp <= 0


player = Player("", 0, 0)
enemy = Enemy("", 0, 0)

name_create()
player_create()

while GameVar.run_ans == "yes":

    for x in range(GameVar.diff_lvl):
        if p_dead():
            break
        mob_round()
    if not p_dead():
        if GameVar.diff_lvl == 1:
            skill_find()
        boss_round()

    if not p_dead():
        next_lvl()
    elif p_dead:
        restart()
