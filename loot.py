from items import generate_bomb
from game_elements import *
import random


def loot_item(item_name, loot_dict):
    loot_dict.setdefault(item_name, 0)
    loot_dict[item_name] += 1


def loot_common(loot_dict):
    common_roll = random.randint(0, 100)
    if common_roll < 70:
        loot_item("Health potion", loot_dict)

    else:
        loot_item(generate_bomb(), loot_dict)


def loot_rare(loot_dict):
    loot_item("Sword", loot_dict)


def loot_legendary(loot_dict):
    loot_item("Golden apple", loot_dict)


def dynamic_percentage(percentage_list, luck):
    formula_x = - 0.5 + (luck / 10)
    formula_b = 1 - (luck / 10)

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


def loot_table_crl(player, loot_dict):
    crl_percentage = [20, 50, 20, 10]
    din_pr = dynamic_percentage(crl_percentage, player.luck)

    loot_roll = random.uniform(0, 100)

    if din_pr[0] <= loot_roll < din_pr[1]:
        loot_common(loot_dict)
    elif din_pr[1] <= loot_roll < din_pr[2]:
        loot_rare(loot_dict)
    elif loot_roll >= din_pr[2]:
        loot_legendary(loot_dict)


def loot_table_cr(player, loot_dict):
    cr_percentage = [20, 55, 25]
    din_pr = dynamic_percentage(cr_percentage, player.luck)

    loot_roll = random.uniform(0, 100)

    if din_pr[0] <= loot_roll < din_pr[1]:
        loot_common(loot_dict)
    elif din_pr[1] <= loot_roll:
        loot_rare(loot_dict)


def sum_loot(loot_dict):
    if loot_dict:
        print(f"You found:")
        for key, value in loot_dict.items():
            if value > 0:
                print(f"{value} {format_items(key)}")
    else:
        print("There was nothing in there.")


def looting(player, mob_class, inventory, move_list):
    loot_ans_list = ("yes", "no")
    lootable_names = ("chest", "pouch")
    loot_question = f"You found a {random.choice(lootable_names)}.\n" \
                    f"Do you want to search it ? {format_ans_lists(loot_ans_list)}"
    loot_ans = check_answer(loot_ans_list, loot_question)

    if loot_ans == "yes":
        loot_dict = {}
        if mob_class == "mob":
            loot_table_cr(player, loot_dict)
        elif mob_class == "boss":
            for i in range(2):
                loot_table_crl(player, loot_dict)
        sum_loot(loot_dict)

        for key, value in loot_dict.items():
            if "items" not in move_list:
                move_list.append("items")
            inventory.setdefault(key, 0)
            inventory[key] += value
