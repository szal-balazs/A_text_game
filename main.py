import random

run_ans = "yes"


class Character:
    def __init__(self, name, hp, dmg):
        self.name = name
        self.hp = hp
        self.dmg = dmg


class Player(Character):
    def attack(self):
        enemy.hp = int(enemy.hp) - int(player.dmg)
        print(f"{enemy.name} has {enemy.hp} hp left.")


class Enemy(Character):
    def attack(self):
        player.hp = int(player.hp) - int(enemy.dmg)
        print(f"Your hp is {player.hp}.")


enemy_name_list = ["Zombie", "Werewolf", "Vampire"]

while run_ans == "yes":
    player_name = input("What is your name?\n")
    player = Player(player_name, 15, 2)
    print(f"Your name is {player.name}")

    enemy_name = random.choice(enemy_name_list)
    enemy = Enemy(enemy_name, 10, 1)

    do_ans = str(input(f"You have been attacked by a {enemy.name}. What do you want to do ? (attack, run)\n"))
    while str(do_ans) not in ["attack", "run"]:
        do_ans = str(input("I don't understand ! Try again (attack, run):\n"))
    if do_ans == "run":
        print("You ran away!")
    while do_ans == "attack":
        player.attack()
        enemy.attack()
        if player.hp or enemy.hp <= 0:
            if enemy.hp <= 0:
                print("You win!")
                do_ans = ""
            elif player.hp <= 0:
                print("You died!")
                do_ans = ""
            else:
                do_ans = str(input("What do you want to do ? (attack, run) \n"))
                while do_ans not in ["attack", "run"]:
                    do_ans = str(input("I don't understand ! Try again (attack, run):\n"))
    if do_ans == "run":
        print("You ran away!")

    run_ans = str(input("Do you want to restart ? (yes or no): \n"))

    while run_ans not in ["yes", "no"]:
        ans = str(input("I don't understand ! Try again: \n"))
    if run_ans == "no":
        print("Bye!")
        exit()
