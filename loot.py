from items import get_item, generate_bomb
from misc import *
import random


def loot_item(item_name):
    get_item(item_name)
    Loot.loot_dict.setdefault(item_name, 0)
    Loot.loot_dict[item_name] += 1


def loot_common():
    common_roll = random.randint(0, 100)
    if common_roll < 70:
        loot_item("Health potion")

    else:
        loot_item(generate_bomb())


def loot_rare():
    loot_item("Sword")


def loot_legendary():
    loot_item("Golden apple")


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


def loot_table_cra(percentages):
    loot_roll = random.uniform(0, 100)

    din_pr = percentages

    if din_pr[0] <= loot_roll < din_pr[1]:
        loot_common()
    elif din_pr[1] <= loot_roll < din_pr[2]:
        loot_rare()
    elif loot_roll >= din_pr[2]:
        loot_legendary()


def loot_table_cr(percentages):
    loot_roll = random.uniform(0, 100)

    din_pr = percentages

    if din_pr[0] <= loot_roll < din_pr[1]:
        loot_common()
    elif din_pr[1] <= loot_roll:
        loot_rare()


def loot_sum():
    if sum(Loot.loot_dict.values()) > 0:
        print(f"You found:")
        for key, value in Loot.loot_dict.items():
            if value > 0:
                print(f"{value} {format_items(key)}")
    else:
        print("There was nothing in there.")

    Loot.loot_dict.clear()


class Loot:
    loot_dict = {}

    cr_percentage = [20, 55, 25]
    cra_percentage = [20, 50, 20, 10]
    ans_list = ("yes", "no")


def looting(luck, mob_class):
    lootable_names = ("chest", "pouch")
    loot_question = f"You found a {random.choice(lootable_names)}.\n" \
                    f"Do you want to search it ? {format_ans_lists(Loot.ans_list)}"
    loot_ans = answer_check(Loot.ans_list, loot_question)

    if loot_ans == "yes":
        if mob_class == "mob":
            perc = dynamic_percentage(Loot.cr_percentage, luck)
            loot_table_cr(perc)
        elif mob_class == "boss":
            for i in range(2):
                perc = dynamic_percentage(Loot.cra_percentage, luck)
                loot_table_cra(perc)
        loot_sum()
