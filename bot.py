import helper

def do_turn(pw):
    (myBest, targetBest, num_ships) = helper.choose_closet_possible(pw)
    pw.debug('Num Ships: ' + str(num_ships))
    pw.debug(myBest.planet_id() + " " + targetBest.planet_id())
    pw.issue_order(myBest, targetBest, num_ships)