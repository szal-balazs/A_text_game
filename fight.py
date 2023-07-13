from items import *
from player import *
from game_elements import check_answer


def print_inventory(inventory):
    print("Your inventory:")

    if any(inventory.values()):
        for key, value in inventory.items():
            if value > 0:
                print(f"{format_items(key)} : {value}")
    else:
        print("Empty")


def how_many_items(item_name, inventory):
    item_count = range(1, inventory[item_name])
    uses = 0
    while uses not in item_count:
        try:
            uses = int(input("How many do you want to use ?\n"))
        except ValueError:
            print("Please enter a whole number.")
        else:
            if uses > inventory[item_name]:
                print(f"You don't have that many {format_items(item_name)}. ")
            else:
                break

    return uses


def end_turn(player, move_ans):
    if move_ans in ("attack", "skills"):
        player.cooldown()


def fighting(player, enemy, inventory):
    print(f"You have been attacked by {format_enemy_name(enemy.name)}.")
    print(enemy)

    while not player.dead() and not enemy.dead():
        fight_question = f"What do you want to do ? {format_ans_lists(player.moves)}"
        move_ans = check_answer(player.moves, fight_question)

        if move_ans != "run":
            if move_ans == "attack":
                player.melee_attack(enemy)
                if not enemy.dead():
                    enemy.attack(player)

            elif move_ans == "items" and "items" in player.moves:
                print_inventory(inventory)
                item_use_ans = input(f"\nWhat item do you want to use (or go{f_back()})\n")
                while item_use_ans not in inventory.keys() and item_use_ans != "back":
                    print_inventory(inventory)
                    item_use_ans = input(f"Try again or go{f_back()})\n")

                if item_use_ans == "Health potion":
                    uses = how_many_items(item_use_ans, inventory)
                    for i in range(uses):
                        use_health_potion(player, inventory),
                elif item_use_ans == "Sword":
                    use_sword(player, inventory)
                elif item_use_ans == "Golden apple":
                    uses = how_many_items(item_use_ans, inventory)
                    for i in range(uses):
                        use_golden_apple(player, inventory)
                elif item_use_ans in ["Holy grenade", "Life bomb", "Fire bomb"]:
                    uses = how_many_items(item_use_ans, inventory)
                    for i in range(uses):
                        use_bomb(item_use_ans, enemy, inventory)

            elif move_ans == "skills" and "skills" in player.moves:
                skill_use_ans = input(f"\nWhat skill do you want to use (or go{f_back()})? "
                                      f"{format_ans_lists(player.skill_list)}:\n")
                while skill_use_ans not in player.skill_list and skill_use_ans != "back":
                    skill_use_ans = input(f"Try again or go{f_back()}."
                                          f"{format_ans_lists(player.skill_list)}\n")
                if skill_use_ans == "Fury":
                    player.fury(enemy)

                if player.skill_used:
                    if not enemy.dead():
                        enemy.attack(player)

            end_turn(player, move_ans)

        elif move_ans == "run":
            print("You ran away!\n")
            break

    player.fury_cd = 0

    if enemy.dead():
        print(f"You won! You defeated the {format_enemy_name(enemy.name)}.\n")
        player.monster_killed += 1

    if player.dead():
        print(f"You died! Monster(s) killed: {player.monster_killed}\n")
