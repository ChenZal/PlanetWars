import random

def choose_closet_possible(pw):
    myPlanets = pw.my_planets()
    targets = []
    for neut in pw.neutral_planets():
        targets.append((neut, False))
    for enemy in pw.enemy_planets():
        targets.append((enemy, True))

    myFleets = pw.my_fleets()
    enemyFleets = pw.enemy_fleets()

    if not myPlanets or not targets:
        return None, None, 0

    haveFound = False
    bestMy = myPlanets[0]
    bestN = targets[0][0]
    bestValue = float('inf')
    num_ships = 0

    for myP in myPlanets:
        for (targ, isEnemy) in targets:
            dist = pw.distance(myP, targ)
            needed = targ.num_ships() + 1
            rate = targ.growth_rate()

            if isEnemy:
                needed += rate * dist

            for myFleet in myFleets:
                if myFleet.destination_planet() == targ.planet_id():
                    needed -= myFleet.num_ships()

            for enemyFleet in enemyFleets:
                if enemyFleet.destination_planet() == targ.planet_id():
                    needed += enemyFleet.num_ships()

            if needed <= 0:
                continue

            # the more distance the worst, the more needed the worst,
            # and the more the rate is the better
            value = (dist + needed) / (rate + 1)
            if (value < bestValue) and needed < myP.num_ships():
                bestValue = value
                bestMy = myP
                bestN = targ
                num_ships = needed

    return bestMy, bestN, num_ships


def do_turn(pw):
    if len(pw.my_planets()) == 0:
        return
    if len(pw.enemy_planets()) == 0:
        return


    myBest, targetBest, num_ships = choose_closet_possible(pw)
    if myBest is None or num_ships == 0:
        return

    #pw.debug('Num Ships: ' + str(num_ships))
    #pw.debug(str(myBest.planet_id()) + " " + str(targetBest.planet_id()))
    pw.issue_order(myBest, targetBest, num_ships)
