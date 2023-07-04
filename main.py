from textgame import *


def main():
    name_create()
    player_create()

    while GameVar.run_ans == "yes":

        for num in range(GameVar.diff_lvl):
            if p_dead():
                break
            mob_round()
        if not p_dead():
            if GameVar.diff_lvl == 1:
                skill_find()
            boss_round()

        if not p_dead():
            next_lvl()
        elif p_dead:
            restart()


if __name__ == "main":
    main()
