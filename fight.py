from items import *


def players_attack(player, enemy):
    enemy.hp = enemy.hp - player.damage()
    print(f"\nYou attacked.")
    print(f"You dealt {player.damage()} damage.")
    if not dead(enemy):
        print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
    else:
        print(f"{format_enemy_name(enemy.name)} has no hp left.\n")


def skill_fury(player, enemy):
    if player.fury_cd == 0:
        enemy_hp_before = [enemy.hp]
        enemy.hp = enemy.hp - player.damage() - player.damage()
        player.skill_used = True
        enemy_hp_after = [enemy.hp]
        fury_dmg = enemy_hp_before[0] - enemy_hp_after[0]
        print(f"\nYou used Fury.")
        print(f"You dealt {fury_dmg} damage.")
        if not dead(enemy):
            print(f"{format_enemy_name(enemy.name)} has {format_stats(enemy.hp)} hp left.\n")
        else:
            print(f"{format_enemy_name(enemy.name)} has no hp left.\n")
    elif player.fury_cd > 0:
        print(f"\nYou can't use this skill for {player.fury_cd} turn(s).\n")
    player.fury_cd = 3


def enemy_attack(player, enemy):
    print(f"{format_enemy_name(enemy.name)} is attacked you.")

    # Special pre damage interactions
    if enemy.name == "Werewolf":
        werewolf_special(enemy)

    # Taking damage
    player.hp = player.hp - enemy_damage(enemy)

    print(f"{enemy.name} dealt {enemy_damage(enemy)} damage to you.")

    # Resetting damage

    if enemy.name == "Werewolf" and enemy.spec_att_timer <= 3:
        enemy.spec_att_timer = 0

    # Special after damage interactions
    if enemy.name == "Vampire":
        vampire_special(enemy)

    # Summary
    if not dead(player):
        print(f"Your hp is {format_stats(player.hp)}.\n")
    else:
        print(f"You have no hp left.\n")


def enemy_damage(enemy):
    if enemy.name == "Werewolf" and enemy.spec_att_timer == 3:
        bonus_dmg = 2
    else:
        bonus_dmg = 0

    return enemy.power + bonus_dmg


def werewolf_special(enemy):
    enemy.spec_att_timer += 1
    if enemy.spec_att_timer == 3:
        print(f"The {format_enemy_name(enemy.name)} slashed you with its claws.")


def vampire_special(enemy):
    v_heal = round(random.randint(0, enemy_damage(enemy)) / 2)
    enemy.hp += v_heal
    if v_heal > 0:
        print(f"{format_enemy_name(enemy.name)} healed {format_stats(v_heal)} hp "
              f"and has {format_stats(enemy.hp)} hp.")
    else:
        print(f"{format_enemy_name(enemy.name)} healed no hp.")


def fight_death_check(player, enemy):
    if dead(player):
        print(f"You died! Monster(s) killed: {player.monster_killed}\n")
        return True
    elif dead(enemy):
        print("You win!\n")
        player.monster_killed += 1
        return True


def cooling_down(player):
    if player.fury_cd > 0:
        player.fury_cd -= 1
    player.skill_used = False


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


def fighting(player, enemy, move_list, inventory):
    skip_list = ["run"]
    fight_question = f"What do you want to do ? {format_ans_lists(move_list)}"

    print(f"You have been attacked by {format_enemy_name(enemy.name)}.")
    print(enemy)
    move_ans = check_answer(move_list, fight_question)

    while move_ans not in skip_list:
        if move_ans == "attack":
            players_attack(player, enemy)
            if not dead(enemy):
                enemy_attack(player, enemy)
            if fight_death_check(player, enemy):
                skip_list.append("exit")
                move_ans = "exit"
            else:
                move_ans = check_answer(move_list, fight_question)

        elif move_ans == "items" and "items" in move_list:
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

            if fight_death_check(player, enemy):
                skip_list.append("exit")
                move_ans = "exit"
            else:
                move_ans = check_answer(move_list, fight_question)

        elif move_ans == "skills" and "skills" in move_list:
            skill_use_ans = input(f"\nWhat skill do you want to use (or go{f_back()})? "
                                  f"{format_ans_lists(player.skill_list)}:\n")
            while skill_use_ans not in player.skill_list and skill_use_ans != "back":
                skill_use_ans = input(f"Try again or go{f_back()}."
                                      f"{format_ans_lists(player.skill_list)}\n")
            if skill_use_ans == "Fury":
                skill_fury(player, enemy)

            if player.skill_used:
                if not dead(enemy):
                    enemy_attack(player, enemy)
                if fight_death_check(player, enemy):
                    skip_list.append("exit")
                    move_ans = "exit"
                else:
                    move_ans = check_answer(move_list, fight_question)
            else:
                move_ans = check_answer(move_list, fight_question)

        if move_ans in ("attack", "skills"):
            cooling_down(player)

    if move_ans == "run":
        print("You ran away!\n")
    if "exit" in skip_list:
        skip_list.remove("exit")
