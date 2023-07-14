def restart(player, inventory):
    answer_list = "yes", "no"
    run_question = f"Do you want to restart ? {format_ans_lists(answer_list)}"
    run_answer = check_ans_bool(run_question)
    if run_answer:
        inventory.clear()
        player.create_stats()
    else:
        print("Bye!")
        exit()


def next_lvl(player, inventory):
    answer_list = "yes", "no"
    next_lvl_question = f"Do you want to go to the next level ? {format_ans_lists(answer_list)}"
    next_lvl_ans = check_ans_bool(next_lvl_question)

    if next_lvl_ans:
        player.diff_lvl += 1
        print(f"\nThe difficulty level is {player.diff_lvl}.\n")
    else:
        restart(player, inventory)


def menu():
    pass


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

def format_skills(ans):
    return f"\033[33m{ans}\033[0m"


def f_back():
    return f"\033[92m back\033[0m"
