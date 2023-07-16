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
                player.turn_end_cooldown()

            elif move_ans == "items" and "items" in player.moves:
                print_inventory(inventory)
                use_item_ans = input(f"\nWhat item do you want to use (or go{f_back()})\n")
                while use_item_ans not in inventory.keys() and use_item_ans != "back":
                    print_inventory(inventory)
                    use_item_ans = input(f"Try again or go{f_back()})\n")

                if use_item_ans == "Health potion":
                    use_health_potion(player, inventory),
                elif use_item_ans == "Sword":
                    use_sword(player, inventory)
                elif use_item_ans == "Golden apple":
                    use_golden_apple(player, inventory)
                elif use_item_ans in ["Holy grenade", "Life bomb", "Fire bomb"]:
                    use_bomb(use_item_ans, enemy, inventory)

            elif move_ans == "skills" and "skills" in player.moves:
                if player.can_use_skill():
                    use_skill_ans = input(f"\nWhich skill do you want to use ? (or go{f_back()}) "
                                          f"{format_ans_lists(player.skill_list)}:\n")
                    while use_skill_ans not in player.skill_list and use_skill_ans != "back":
                        use_skill_ans = input(f"Try again or go{f_back()}."
                                              f"{format_ans_lists(player.skill_list)}\n")

                    if use_skill_ans == "Fury" and player.fury_cd == 0:
                        player.fury(enemy)
                        if not enemy.dead():
                            enemy.attack(player)
                    else:
                        print(f"\nYou can't use this skill for {player.fury_cd} turn(s).\n")

                    if player.skill_used:
                        player.turn_end_cooldown()

        elif move_ans == "run":
            print("You ran away!\n")
            break

    player.reset_cooldown()

    if enemy.dead():
        print(f"You won! You defeated the {format_enemy_name(enemy.name)}.\n")
        player.monster_killed += 1

    if player.dead():
        print(f"You died! Monster(s) killed: {player.monster_killed}\n")
