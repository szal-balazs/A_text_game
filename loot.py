from textgame import *
import random


def loot_common():
    common_roll = random.randint(0, 100)
    if common_roll < 70:
        get_item("Health potion")
        loot_dict["Health potion"] += 1
    else:
        get_item(generate_bomb())
        loot_dict[generate_bomb()] += 1


def loot_rare():
    get_item("Sword")
    loot_dict["Sword"] += 1


def loot_legendary():
    get_item("Golden apple")
    loot_dict["Golden apple"] += 1


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


def loot_table_cra():
    loot_roll = random.uniform(0, 100)

    percentage = [20, 50, 20, 10]
    din_pr = dynamic_percentage(percentage)

    if din_pr[0] <= loot_roll < din_pr[1]:
        loot_common()
    elif din_pr[1] <= loot_roll < din_pr[2]:
        loot_rare()
    elif loot_roll >= din_pr[2]:
        loot_legendary()


def loot_table_cr():
    loot_roll = random.uniform(0, 100)

    percentage = [20, 55, 25]
    din_pr = dynamic_percentage(percentage)

    if din_pr[0] <= loot_roll < din_pr[1]:
        loot_common()
    elif din_pr[1] <= loot_roll:
        loot_rare()


loot_dict = {
    "Health potion": 0,
    "Sword": 0,
    "Golden apple": 0,
    "Holy grenade": 0,
    "Life bomb": 0,
    "Fire bomb": 0
}


def loot_sum():
    if sum(loot_dict.values()) > 0:
        print(f"You found:")
        for key, value in loot_dict.items():
            if value > 0:
                print(f"{value} {format_items(key)}")
    else:
        print("There was nothing in there.")


def looting():
    lootable_names = ("chest", "pouch")
    loot_question = f"You found a {random.choice(lootable_names)}.\n" \
                    f"Do you want to search it ? {format_ans_lists(GameVar.ans_list)}"
    loot_ans = answer_check(GameVar.ans_list, loot_question)

    if loot_ans == "yes":
        if enemy.mob_class == "mob":
            loot_table_cr()
        elif enemy.mob_class == "boss":
            for x in range(2):
                loot_table_cra()
        loot_sum()
