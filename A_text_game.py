import random


class Character:
    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.power = power


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


# Player setup ----------------------------------------------------
class Player(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.max_hp = 20
        self.luck = 0
        self.max_luck = 8
        self.bonus_dmg = 0
        self.damage = self.power + self.bonus_dmg

    @classmethod
    def attack(cls):
        enemy.hp = enemy.hp - player.damage
        print(f"\nYou attacked.")
        print(f"You dealt {player.damage} damage.")
        if not e_dead():
            print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(enemy.name)} has no hp left.\n")

    skill_list = []
    skill_used = "no"

    fury_cd = 0

    @classmethod
    def skill_fury(cls):
        if player.fury_cd == 0:
            enemy_hp_before = [enemy.hp]
            enemy.hp = enemy.hp - player.damage - player.damage
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

    @classmethod
    def name_create(cls):
        player.name = input("What is your name?\n")
        if len(player.name) == 0:
            player.name = "Anon"
        print(f"Your name is {format_stats(player.name)}.\n")

    @classmethod
    def create(cls):
        player.hp = 20
        player.power = 3

    @classmethod
    def stat(cls):
        stat = {
            "Name": player.name,
            "HP": player.hp,
            "Power": player.power,
            "Damage": player.damage
        }

        print(f"\nYour stats are:")
        for key in stat.keys():
            print(f"{format_stats_name(key)} : {format_stats(stat[key])}")


move_list = ["attack", "run"]


# Enemy setup -----------------------------------------------------
class Enemy(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.mob_class = ""
        self.type = ""

    spec_att_timer = 0

    @classmethod
    def generate_enemy(cls):
        enemy_name_list = ["Zombie", "Werewolf", "Vampire"]
        enemy.name = random.choice(enemy_name_list)
        enemy.hp = 10
        enemy.power = 2
        enemy.mob_class = "mob"
        enemy.type = enemy.type_def()

    @classmethod
    def generate_boss(cls):
        enemy_name_list = ["Dark Troll", "Necromancer", "Mad Tree"]
        enemy.name = random.choice(enemy_name_list)
        enemy.hp = 13
        enemy.power = 3
        enemy.mob_class = "boss"
        enemy.type = enemy.type_def()

    # Mob Types
    unholy = ("Vampire", "Dark Troll")
    undead = ("Zombie", "Necromancer")
    creature = ("Werewolf", "Mad Tree")

    @staticmethod
    def type_def():
        if enemy.name in Enemy.unholy:
            return "Unholy"
        elif enemy.name in Enemy.undead:
            return "Undead"
        elif enemy.name in Enemy.creature:
            return "Creature"

    @classmethod
    def stat(cls):
        e_stat = {
            "Name": enemy.name,
            "HP": enemy.hp,
            "Power": enemy.power,
            "Type": enemy.type
        }

        for key in e_stat.keys():
            print(f"{format_stats_name(key)} : {format_stats(e_stat[key])}")

    @classmethod
    def attack(cls):
        print(f"{format_enemy_name(enemy.name)} is attacked you.")

        # Special pre damage interactions
        if enemy.name == "Werewolf":
            enemy.werewolf_special()

        # Taking damage
        player.hp = int(player.hp) - int(enemy.damage())

        print(f"{enemy.name} dealt {enemy.damage()} damage to you.")

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

    @classmethod
    def damage(cls):
        if enemy.name == "Werewolf" and Enemy.spec_att_timer == 3:
            bonus_dmg = 2
        else:
            bonus_dmg = 0

        return int(enemy.power) + bonus_dmg

    @classmethod
    def werewolf_special(cls):
        Enemy.spec_att_timer += 1
        if Enemy.spec_att_timer == 3:
            print(f"The {format_enemy_name(enemy.name)} slashed you with its claws.")

    @classmethod
    def vampire_special(cls):
        v_heal = round(random.randint(0, int(enemy.damage())) / 2)
        enemy.hp += v_heal
        print(f"{enemy.name} healed {format_stats(v_heal)} hp and has {format_stats(enemy.hp)} hp.")


# Items ----------------------------------------------------------------

class Item:

    def __init__(self, name):
        self.name = name

    def get_item(self):
        if "items" not in move_list:
            move_list.append("items")
        if self.name not in GameVar.inventory_dict:
            GameVar.inventory_dict[self.name] = 1
        else:
            GameVar.inventory_dict[self.name] += 1

    @classmethod
    def use_health_potion(cls):
        if GameVar.inventory_dict[health_potion.name] <= 0:
            print(f"You have no {format_items(health_potion.name)}")
        else:
            GameVar.inventory_dict[health_potion.name] -= 1
            heal = 5
            heal = min(heal, player.max_hp - player.hp)
            player.hp += heal
            print(f"You healed {heal} hp. Your hp is {format_stats(player.hp)} now.\n")

    @classmethod
    def use_sword(cls):
        if "sword" not in GameVar.equipped:
            if sword.name not in GameVar.inventory_dict:
                print(f"You have no {format_items(sword.name)}")
            else:
                GameVar.inventory_dict[sword.name] -= 1
                player.bonus_dmg += 2
                GameVar.equipped.append("Sword")
                print(f"You equipped the sword. You have {format_stats(player.damage)} damage now.\n")
        else:
            print(f"You already have a {format_items(sword.name)} equipped.\n")

    @classmethod
    def use_golden_apple(cls):
        if GameVar.inventory_dict[golden_apple.name] <= 0:
            print(f"You have no {format_items(golden_apple.name)}")
        else:
            GameVar.inventory_dict[golden_apple.name] -= 1
            player.max_hp += 4
            print(f"You maximum hp increased with 4. It is now {format_stats(player.max_hp)}.\n")


class Bomb(Item):

    @classmethod
    def generate_bomb(cls):

        bomb_names = ("Holy grenade", "Life bomb", "Fire bomb")
        bomb.name = random.choice(bomb_names)

    @classmethod
    def use_bomb(cls):

        GameVar.inventory_dict[bomb.name] -= 1

        def is_weak():

            conditions = {
                "Holy grenade": "Unholy",
                "Life bomb": "Undead",
                "Fire bomb": "Creature"
            }
            return enemy.type == conditions.get(bomb.name, False)

        enemy.hp -= 6 if is_weak() else 3
        print(f"You dealt {6 if is_weak() else 3} damage.")

        if not e_dead():
            print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(enemy.name)} has no hp left.\n")


def inventory_print():
    print("Your inventory:")

    if any(GameVar.inventory_dict.values()):
        for key, value in GameVar.inventory_dict.items():
            if value > 0:
                print(f"{format_items(key)} : {value}")
    else:
        print("Empty")


# Game components -------------------------------------------------------

def answer_check(answer_list, question):
    while (answer := input(f"{question}:\n")) not in answer_list:
        print(f"I don't understand !\n")
    return answer


def fight():
    print(f"You have been attacked by {format_enemy_name(enemy.name)}.")
    enemy.stat()
    skip_list = ["run"]
    fight_question = f"What do you want to do ? {format_ans_lists(move_list)}"
    move_ans = answer_check(move_list, fight_question)

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
            player.attack()
            if not e_dead():
                enemy.attack()
            if fight_death_check():
                skip_list.append("exit")
                move_ans = "exit"
            else:
                move_ans = answer_check(move_list, fight_question)

        if "items" in move_list:
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
                    move_ans = answer_check(move_list, fight_question)

        if "skills" in move_list:
            if move_ans == "skills":
                skill_use_ans = input(f"\nWhat skill do you want to use (or go{f_back()})? "
                                      f"{format_ans_lists(player.skill_list)}:\n")
                while skill_use_ans not in player.skill_list and skill_use_ans != "back":
                    skill_use_ans = input(f"Try again or go{f_back()}."
                                          f"{format_ans_lists(player.skill_list)}\n")
                if skill_use_ans == "Fury":
                    player.skill_fury()

                if player.skill_used == "yes":
                    if not e_dead():
                        enemy.attack()
                    if fight_death_check():
                        skip_list.append("exit")
                        move_ans = "exit"
                    else:
                        move_ans = answer_check(move_list, fight_question)
                else:
                    move_ans = answer_check(move_list, fight_question)
        turn_end()

    if move_ans == "run":
        print("You ran away!\n")
    if "exit" in skip_list:
        skip_list.remove("exit")


def looting():
    def loot_common():
        common_roll = random.randint(0, 100)
        if common_roll < 70:
            health_potion.get_item()
            loot_dict["Health potion"] += 1
        else:
            bomb.generate_bomb()
            bomb.get_item()
            loot_dict[bomb.name] += 1

    def loot_rare():
        sword.get_item()
        loot_dict["Sword"] += 1

    def loot_legendary():
        golden_apple.get_item()
        loot_dict["Golden apple"] += 1

    def dynamic_percentage(percentage_list):

        formula_x = - 0.5 + (player.luck / 10)
        formula_b = 1 - (player.luck / 10)

        distance_in_x = [0]
        temp = 0
        for num in percentage_list:
            temp = round(2 * num / 100 + temp, 3)
            distance_in_x.append(temp)

        heights = [round(formula_x * distance_in_x[num] + formula_b, 3) for num in range(len(distance_in_x))]

        areas = [round((heights[num] + heights[num + 1]) / 2 * distance_in_x[num + 1], 3)
                 for num in range(len(heights) - 1)]

        dyn_perc = [round(sum(areas[:num]) / sum(areas) * 100, 2) for num in range(1, len(areas))]

        return dyn_perc

    def loot_table_cra():
        loot_roll = random.uniform(0, 100)

        percentage = [20, 50, 20, 10]
        din_pr = dynamic_percentage(percentage)

        if din_pr[0] <= loot_roll < din_pr[1]:
            loot_common()
        elif din_pr[1] <= loot_roll < din_pr[2]:
            loot_rare()
        elif loot_roll >= din_pr[2]:
            loot_legendary()

    def loot_table_cr():
        loot_roll = random.uniform(0, 100)

        percentage = [20, 55, 25]
        din_pr = dynamic_percentage(percentage)

        if din_pr[0] <= loot_roll < din_pr[1]:
            loot_common()
        elif din_pr[1] <= loot_roll:
            loot_rare()

    loot_dict = {
        "Health potion": 0,
        "Sword": 0,
        "Golden apple": 0,
        "Holy grenade": 0,
        "Life bomb": 0,
        "Fire bomb": 0
    }

    def loot_sum():

        if sum(loot_dict.values()) > 0:
            print(f"You found:")
            for key, value in loot_dict.items():
                if value > 0:
                    print(f"{value} {format_items(key)}")
        else:
            print("There was nothing in there.")

    lootable_names = ("chest", "pouch")
    loot_question = f"You found a {random.choice(lootable_names)}.\n" \
                    f"Do you want to search it ? {format_ans_lists(GameVar.ans_list)}"
    loot_ans = answer_check(GameVar.ans_list, loot_question)

    if loot_ans == "yes":
        if enemy.mob_class == "mob":
            loot_table_cr()
        elif enemy.mob_class == "boss":
            for x in range(2):
                loot_table_cra()
        loot_sum()


def skill_find():
    skill_question = f"\nYou found a book. Do you want to learn a new skill ?" \
                     f" {format_ans_lists(GameVar.ans_list)}"
    skill_ans = answer_check(GameVar.ans_list, skill_question)
    if skill_ans == "yes":
        if "skills" not in move_list:
            move_list.append("skills")
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
        player.create()


def mob_round():
    player.stat()
    enemy.generate_enemy()
    fight()
    if not p_dead():
        looting()


def boss_round():
    player.stat()
    enemy.generate_boss()
    fight()
    if not p_dead():
        looting()


def next_lvl():
    next_lvl_question = f"Do you want to go to the next level ? {format_ans_lists(GameVar.ans_list)}"
    next_lvl_ans = answer_check(GameVar.ans_list, next_lvl_question)

    if next_lvl_ans == "no":
        restart()
    elif next_lvl_ans == "yes":
        GameVar.diff_lvl += 1


# Game ---------------------------------
# Generation
# Items
bomb = Bomb("")
health_potion = Item("Health potion")
sword = Item("Sword")
golden_apple = Item("Golden apple")

# Player
player = Player("", 0, 0)
player.name_create()
player.create()


class GameVar:
    run_ans = "yes"
    ans_list = ("yes", "no")
    diff_lvl = 1
    monster_killed = 0
    inventory_dict = {}
    equipped = []


def p_dead():
    return player.hp <= 0


def e_dead():
    return enemy.hp <= 0


while GameVar.run_ans == "yes":

    print(f"\nThe difficulty level is {GameVar.diff_lvl}.\n")

    enemy = Enemy("", 0, 0)

    for i in range(GameVar.diff_lvl):
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
