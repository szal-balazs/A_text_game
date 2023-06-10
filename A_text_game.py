import random


class Character:
    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.power = power


def format_ans_lists(ans):
    y = ', '.join(ans)
    x = f"\033[92m {y} \033[0m"
    return x


# Player setup ----------------------------------------------------
class Player(Character):

    @classmethod
    def attack(cls):
        enemy.hp = int(enemy.hp) - int(player.power)
        print(f"You attacked.\n"
              f"{enemy.name} has {enemy.hp} hp left.")

    @classmethod
    def name_create(cls):
        player.name = input("What is your name?\n")
        print(f"Your name is {player.name}.\n")

    @classmethod
    def create(cls):
        player.hp = 15
        player.power = 4

    @classmethod
    def stat(cls):
        stat = {
            "Name": player.name,
            "HP": player.hp,
            "Power": player.power
        }
        print(f"Your stats are:")
        print(f"{stat}\n")


move_list = ["attack", "run"]


# Enemy setup -----------------------------------------------------
class Enemy(Character):

    @classmethod
    def attack(cls):
        player.hp = int(player.hp) - int(enemy.power)
        print(f"{enemy.name} is attacked you.\n"
              f"Your hp is {player.hp}.\n")

    @classmethod
    def generate_enemy(cls):
        enemy_name_list = ["Zombie", "Werewolf", "Vampire"]
        enemy.name = random.choice(enemy_name_list)
        enemy.hp = 10
        enemy.power = 2

    @classmethod
    def stat(cls):
        e_stat = {
            "Name": enemy.name,
            "HP": enemy.hp,
            "Power": enemy.power
        }
        print(f"{e_stat}\n")


# Items ----------------------------------------------------------------

class Item:

    def __init__(self, name):
        self.name = name

    def get_item(self):
        if "items" not in move_list:
            move_list.append("items")
        inventory.append(self.name)
        inventory_dict[self.name] = inventory.count(self.name)


def use_health_p():
    heal = 5
    max_heal = player.hp + heal
    if max_heal > 15:
        heal = 15 - player.hp
    player.hp += heal
    inventory.remove("Health potion")
    inventory_dict["Health potion"] = inventory.count("Health potion")
    print(f"You healed {heal} hp. Your hp is {player.hp}.\n")


def use_sword():
    if "sword" not in equipped:
        player.power += 2
        inventory.remove("Sword")
        inventory_dict["Sword"] = inventory.count("Sword")
        equipped.append("Sword")
        print(f"You equipped the sword. Your power is {player.power} now.\n")
    if "sword" in equipped:
        print("You already have a sword equipped.\n")


health_potion = Item("Health potion")
sword = Item("Sword")


# Game components -------------------------------------------------------

def answer_check(answer_list, question):
    answer = input(f"{question}:\n")
    while answer not in answer_list:
        answer = input(f"I don't understand !\n{question}:\n")
    return answer


def fight():
    print(f"You have been attacked by {enemy.name}.")
    enemy.stat()
    skip_list = ["run"]
    fight_question = f"What do you want to do ?{format_ans_lists(move_list)}"
    move_ans = answer_check(move_list, fight_question)

    while move_ans not in skip_list:
        while move_ans == "attack":
            global monster_killed
            player.attack()
            enemy.attack()
            if player.hp <= 0:
                print(f"You died! Monster(s) killed: {format_ans_lists(monster_killed)}\n")
                skip_list.append("exit")
                move_ans = "exit"
            elif enemy.hp <= 0:
                print("You win!\n")
                monster_killed += 1
                move_ans = "exit"
                skip_list.append("exit")
            else:
                move_ans = answer_check(move_list, fight_question)
        if "items" in move_list:
            while move_ans == "items":
                print(f"Your inventory:")
                print(inventory_dict)
                item_use_ans = input(f"What item do you want to use (or go\033[92m back\033[0m)?\n")
                while item_use_ans not in inventory:
                    if item_use_ans == "back":
                        break
                    else:
                        item_use_ans = str(input(f"I don't understand !\n"
                                                 f"Your inventory:\n"
                                                 f"{inventory_dict}\n"
                                                 f" Try again or go\033[92m back\033[0m):\n"))
                if item_use_ans == "Health potion":
                    use_health_p()
                elif item_use_ans == "Sword":
                    use_sword()
                move_ans = input(f"What do you want to do ? {move_list}\n")
                while move_ans not in move_list:
                    move_ans = str(input(f"I don't understand ! Try again {move_list}:\n"))
    if move_ans == "run":
        print("You ran away!\n")
    if "exit" in skip_list:
        skip_list.remove("exit")


def chest():
    chest_question = f"You found a chest. Do you want to open it ? {format_ans_lists(ans_list)}"
    chest_ans = answer_check(ans_list, chest_question)

    if chest_ans == "yes":
        loot_roll = random.randint(1, 100)
        if loot_roll <= 20:
            print("There is nothing in there.\n")
        elif 20 < loot_roll <= 90:
            health_potion.get_item()
            print(f"You found a {health_potion.name}.\n")
        elif loot_roll >= 90:
            sword.get_item()
            print(f"You found a {sword.name}.\n")


def restart():
    global run_ans
    run_question = f"Do you want to restart ? {format_ans_lists(ans_list)}:"
    run_ans = answer_check(ans_list, run_question)
    if run_ans == "no":
        print("Bye!")
        exit()
    elif run_ans == "yes":
        global diff_lvl
        diff_lvl = 1
        inventory.clear()
        inventory_dict.clear()
        player.create()


def rounds():
    player.stat()
    enemy.generate_enemy()
    fight()
    if not dead():
        chest()


def next_lvl():
    next_lvl_question = f"Do you want to go to the next level ? {format_ans_lists(ans_list)}:"
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
inventory = []
inventory_dict = {}
equipped = []


def dead():
    if player.hp > 0:
        return False
    if player.hp <= 0:
        return True


while run_ans == "yes":

    enemy = Enemy("", 0, 0)

    print(f"The difficulty level is {diff_lvl}.\n")

    for i in range(diff_lvl):
        if dead():
            break
        rounds()

    if not dead():
        next_lvl()
    elif dead:
        restart()
