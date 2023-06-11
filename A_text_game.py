import random


class Character:
    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.power = power


# Formats -----------------------------------------------------------
def format_ans_lists(ans):
    y = ', '.join(ans)
    x = f"\033[92m {y}\033[0m"
    return x


def format_stats(ans):
    x = f"\033[36m{ans}\033[0m"
    return x


def format_enemy_name(ans):
    x = f"\033[31m{ans}\033[0m"
    return x


def format_items(ans):
    x = f"\033[92m{ans}\033[0m"
    return x


# Player setup ----------------------------------------------------
class Player(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.max_hp = 20

    @classmethod
    def attack(cls):
        enemy.hp = int(enemy.hp) - int(player.damage())
        print(f"\nYou attacked.")
        print(f"You dealt {player.damage()} damage.")
        if not e_dead():
            print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(enemy.name)} has no hp left.\n")

    @classmethod
    def damage(cls):
        if False:
            pass
        else:
            dmg = int(player.power)
        return dmg

    fury_cd = 0

    @classmethod
    def skill_fury(cls):
        pass

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
            "Power": player.power
        }

        key_format = "\033[34m"
        value_format = "\033[36m"
        key_format_end = "\033[0m"
        print(f"\nYour stats are:")
        for key in stat.keys():
            print(key_format, key, ":", value_format, stat[key], key_format_end)


move_list = ["attack", "run"]


# Enemy setup -----------------------------------------------------
class Enemy(Character):

    def __init__(self, name, hp, power):
        super().__init__(name, hp, power)
        self.mob_class = ""
        self.type = ""

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

        key_format = "\033[34m"
        value_format = "\033[36m"
        key_format_end = "\033[0m"
        for key in e_stat.keys():
            print(key_format, key, ":", value_format, e_stat[key], key_format_end)

    spec_att_timer = 0

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
        dmg = int(enemy.power) + bonus_dmg
        return dmg

    @classmethod
    def werewolf_special(cls):
        Enemy.spec_att_timer += 1
        if Enemy.spec_att_timer == 3:
            print(f"The {format_enemy_name(enemy.name)} slashed you with its claws.")

    @classmethod
    def vampire_special(cls):
        v_heal = round(random.randint(0, int(enemy.damage()))/2)
        enemy.hp += v_heal
        print(f"{enemy.name} healed {format_stats(v_heal)} hp and has {format_stats(enemy.hp)} hp.")


# Items ----------------------------------------------------------------

class Item:

    def __init__(self, name):
        self.name = name

    def get_item(self):
        if "items" not in move_list:
            move_list.append("items")
        if self.name not in inventory_dict:
            inventory_dict[self.name] = 1
        else:
            inventory_dict[self.name] += 1

    @classmethod
    def use_h_potion(cls):
        if inventory_dict[health_potion.name] <= 0:
            print(f"You have no {format_items(health_potion.name)}")
        else:
            inventory_dict[health_potion.name] -= 1
            heal = 5
            max_heal = player.hp + heal
            if max_heal > player.max_hp:
                heal = player.max_hp - player.hp
            player.hp += heal
            print(f"You healed {heal} hp. Your hp is {format_stats(player.hp)}.\n")

    @classmethod
    def use_sword(cls):
        if "sword" not in equipped:
            if sword.name not in inventory_dict:
                print(f"You have no {format_items(sword.name)}")
            else:
                inventory_dict[sword.name] -= 1
                player.power += 2
                equipped.append("Sword")
                print(f"You equipped the sword. Your power is {format_stats(player.power)} now.\n")
        if "sword" in equipped:
            print(f"You already have a {format_items(sword.name)} equipped.\n")

    @classmethod
    def use_golden_apple(cls):
        if inventory_dict[golden_apple.name] <= 0:
            print(f"You have no {format_items(health_potion.name)}")
        else:
            inventory_dict[golden_apple.name] -= 1
            player.max_hp += 4
            print(f"You maximum hp increased with 4. Your maximum hp is {format_stats(player.max_hp)}.\n")


class Bomb(Item):

    @classmethod
    def generate_bomb(cls):

        bomb_names = ("Holy grenade", "Life bomb", "Fire bomb")
        bomb.name = random.choice(bomb_names)

    @classmethod
    def use_bomb(cls):

        inventory_dict[bomb.name] -= 1

        def is_weak():
            if enemy.type == "Unholy" and bomb.name == "Holy grenade":
                return True
            elif enemy.type == "Undead" and bomb.name == "Life bomb":
                return True
            elif enemy.type == "Creature" and bomb.name == "Fire bomb":
                return True
            else:
                return False

        if is_weak():
            enemy.hp -= 6
            print("You dealt 6 damage.")
        else:
            enemy.hp -= 3
            print("You dealt 3 damage.")
        if not e_dead():
            print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(enemy.name)} has no hp left.\n")


# Generate items ----
bomb = Bomb("")
health_potion = Item("Health potion")
sword = Item("Sword")
golden_apple = Item("Golden apple")


def inventory_print():
    key_format = "\033[92m"
    key_format_end = "\033[0m"
    print(f"Your inventory:")

    if sum(inventory_dict.values()) > 0:
        for key in inventory_dict:
            if inventory_dict[key] > 0:
                print(key_format, key, key_format_end, ":", inventory_dict[key])
    else:
        print("Empty")


# Game components -------------------------------------------------------

def answer_check(answer_list, question):
    answer = input(f"{question}:\n")
    while answer not in answer_list:
        answer = input(f"I don't understand !\n{question}:\n")
    return answer


def fight():
    print(f"You have been attacked by {format_enemy_name(enemy.name)}.")
    enemy.stat()
    skip_list = ["run"]
    fight_question = f"What do you want to do ?{format_ans_lists(move_list)}"
    move_ans = answer_check(move_list, fight_question)

    def fight_death_check():
        global monster_killed
        if p_dead():
            print(f"You died! Monster(s) killed: {monster_killed}\n")
            return True
        elif e_dead():
            print("You win!\n")
            monster_killed += 1
            return True

    while move_ans not in skip_list:
        while move_ans == "attack":
            global monster_killed
            player.attack()
            if not e_dead():
                enemy.attack()
            if fight_death_check():
                skip_list.append("exit")
                move_ans = "exit"
            else:
                move_ans = answer_check(move_list, fight_question)
        if "items" in move_list:
            while move_ans == "items":
                inventory_print()
                item_use_ans = input(f"\nWhat item do you want to use (or go\033[92m back\033[0m)?\n")
                while item_use_ans not in inventory_dict.keys():
                    if item_use_ans == "back":
                        break
                    else:
                        inventory_print()
                        item_use_ans = input(f"Try again or go\033[92m back\033[0m\n")

                if item_use_ans == "Health potion":
                    health_potion.use_h_potion()
                elif item_use_ans == "Sword":
                    sword.use_sword()
                elif item_use_ans == "Golden apple":
                    golden_apple.use_golden_apple()
                elif item_use_ans in ("Holy grenade", "Life bomb", "Fire bomb"):
                    bomb.name = item_use_ans
                    bomb.use_bomb()

                if fight_death_check():
                    skip_list.append("exit")
                    move_ans = "exit"
                else:
                    move_ans = answer_check(move_list, fight_question)

    if move_ans == "run":
        print("You ran away!\n")
    if "exit" in skip_list:
        skip_list.remove("exit")


def looting():
    lootable_names = ("chest", "pouch")
    loot_question = f"You found a {random.choice(lootable_names)}.\n" \
                    f"Do you want to search it ? {format_ans_lists(ans_list)}"
    loot_ans = answer_check(ans_list, loot_question)

    def loot_table():
        # loot common item
        if 10 <= loot_roll < 41:
            health_potion.get_item()
            loot_dict["Health potion"] += 1
        elif 41 <= loot_roll < 79:
            bomb.generate_bomb()
            bomb.get_item()
            loot_dict[bomb.name] += 1
        # loot rare item
        elif 80 <= loot_roll > 99:
            sword.get_item()
            loot_dict["Sword"] += 1
            # loot legendary item
        elif 99 < loot_roll:
            golden_apple.get_item()
            loot_dict["Golden apple"] += 1

    loot_dict = {
        "Health potion": 0,
        "Sword": 0,
        "Golden apple": 0,
        "Holy grenade": 0,
        "Life bomb": 0,
        "Fire bomb": 0
    }

    def loot_sum():
        key_format = "\033[92m"
        key_format_end = "\033[0m"

        if sum(loot_dict.values()) > 0:
            print(f"You found:")
            for key in loot_dict:
                if loot_dict[key] > 0:
                    print(loot_dict[key], key_format, key, key_format_end)
        else:
            print("There was nothing in there.")

    if loot_ans == "yes":
        loot_roll = 0
        if enemy.mob_class == "mob":
            loot_roll = random.randint(0, 79)
            loot_table()
        if enemy.mob_class == "boss":
            for x in range(2):
                loot_roll = random.randint(0, 100)
                loot_table()
        loot_sum()


def restart():
    global run_ans
    run_question = f"Do you want to restart ? {format_ans_lists(ans_list)}"
    run_ans = answer_check(ans_list, run_question)
    if run_ans == "no":
        print("Bye!")
        exit()
    elif run_ans == "yes":
        global diff_lvl
        diff_lvl = 1
        inventory_dict.clear()
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
    next_lvl_question = f"Do you want to go to the next level ? {format_ans_lists(ans_list)}"
    next_lvl_ans = answer_check(ans_list, next_lvl_question)

    if next_lvl_ans == "no":
        restart()
    elif next_lvl_ans == "yes":
        global diff_lvl
        diff_lvl += 1


# Game ---------------------------------

run_ans = "yes"
ans_list = ("yes", "no")

player = Player("", 0, 0)
player.name_create()
player.create()

diff_lvl = 1
monster_killed = 0
inventory_dict = {}
equipped = []


def p_dead():
    if player.hp > 0:
        return False
    if player.hp <= 0:
        return True


def e_dead():
    if enemy.hp > 0:
        return False
    if enemy.hp <= 0:
        return True


while run_ans == "yes":

    print(f"\nThe difficulty level is {diff_lvl}.\n")

    enemy = Enemy("", 0, 0)

    for i in range(diff_lvl):
        if p_dead():
            break
        mob_round()
    if not p_dead():
        boss_round()

    if not p_dead():
        next_lvl()
    elif p_dead:
        restart()
