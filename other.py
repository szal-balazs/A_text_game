def inventory_print(inventory):
    print("Your inventory:")

    if any(inventory.values()):
        for key, value in inventory.items():
            if value > 0:
                print(f"{format_items(key)} : {value}")
    else:
        print("Empty")


def check_answer(answer_list, question):
    while (answer := input(f"{question}:\n")) not in answer_list:
        print(f"I don't understand !\n")
    return answer


def check_ans_bool(question):
    while (answer := input(f"{question}:\n")) not in ("yes", "no"):
        print(f"I don't understand !\n")

    if answer == "yes":
        return True
    else:
        return False


def format_ans_lists(ans):
    return f"\033[92m{', '.join(ans)}\033[0m"


def format_stats(ans):
    return f"\033[36m{ans}\033[0m"


def format_stats_name(ans):
    return f"\033[34m{ans}\033[0m"


def format_enemy_name(ans):
    return f"\033[31m{ans}\033[0m"


def format_items(ans):
    return f"\033[92m{ans}\033[0m"


def f_back():
    return f"\033[92m back\033[0m"


def enemy_stat(enemy):
    e_stat = {
        "Name": enemy.name,
        "HP": enemy.hp,
        "Power": enemy.power,
        "Type": enemy.type
    }

    for key in e_stat.keys():
        print(f"{format_stats_name(key)} : {format_stats(e_stat[key])}")


def player_stat(player):
    stat = {
        "Name": player.name,
        "HP": player.hp,
        "Power": player.power,
        "Damage": player.damage()
    }

    print(f"\nYour stats are:")
    for key in stat.keys():
        print(f"{format_stats_name(key)} : {format_stats(stat[key])}")