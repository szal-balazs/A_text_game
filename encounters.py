from game_elements import *
from loot import looting
from fight import fighting


def find_skill(player, move_list):
    answer_list = "yes", "no"
    skill_question = f"You found a book. Do you want to learn a new skill ?" \
                     f" {format_ans_lists(answer_list)}"
    skill_ans = check_ans_bool(skill_question)
    if skill_ans:
        if "skills" not in move_list:
            move_list.append("skills")
        player.skill_list.append("Fury")
        print("You learned a new skill.")


def fighting_round(player, enemy, mob_type, move_list, inventory):
    print(player)
    generate_enemy(enemy, mob_type, player.diff_lvl)
    fighting(player, enemy, move_list, inventory)
    if not dead(player):
        looting(player, mob_type, inventory, move_list)
