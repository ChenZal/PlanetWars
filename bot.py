import helper

def do_turn(pw):
    if len(pw.my_planets()) == 0:
        return
    (myBest, targetBest, num_ships) = helper.choose_closet_possible(pw)
    pw.debug('Num Ships: ' + str(num_ships))
    pw.debug(str(myBest.planet_id()) + " " + str(targetBest.planet_id()))
    pw.issue_order(myBest, targetBest, num_ships)