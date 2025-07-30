from helper import *


def do_turn(pw):
    if len(pw.my_planets()) == 0:
        return
    if len(pw.enemy_planets()) == 0:
        return

    myBest, targetBest, num_ships = choose_closet_possible(pw)
    if myBest is None or num_ships == 0:
        return
    if myBest not in pw.my_planets():
        return

    #pw.debug('Num Ships: ' + str(num_ships))
    #pw.debug(str(myBest.planet_id()) + " " + str(targetBest.planet_id()))
    pw.issue_order(myBest, targetBest, num_ships)
