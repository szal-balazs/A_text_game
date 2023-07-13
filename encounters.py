from game_elements import *
from loot import looting
from fight import fighting


def find_skill(player):
    answer_list = "yes", "no"
    skill_question = f"You found a book. Do you want to learn a new skill ?" \
                     f" {format_ans_lists(answer_list)}"
    skill_ans = check_ans_bool(skill_question)
    if skill_ans:
        if "skills" not in player.moves:
            player.moves.append("skills")
        player.skill_list.append("Fury")
        print("You learned a new skill.")


def fighting_round(player, enemy, mob_type, inventory):
    print(player)
    enemy.generate(player, mob_type)
    fighting(player, enemy, inventory)
    if not player.dead():
        looting(player, mob_type, inventory)
