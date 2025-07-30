from random import randint

# 1- mine, 2 -enemy, 3-neutral
NEUTRAL = 3
ENEMY = 2
MINE = 1

def choose_closet_possible(pw):
    myPlanets = pw.my_planets()
    myFleets = pw.my_fleets()
    enemyFleets = pw.enemy_fleets()

    if not myPlanets:
        return None, None, 0

    # defense
    for planet in myPlanets:
        incoming_enemy_ships = sum(
            fleet.num_ships()
            for fleet in enemyFleets
            if fleet.destination_planet() == planet.planet_id()
        )
        incoming_my_ships = sum(
            fleet.num_ships()
            for fleet in myFleets
            if fleet.destination_planet() == planet.planet_id()
        )
        net_threat = incoming_enemy_ships - incoming_my_ships
        if net_threat > 0:
            closest_source = None
            min_dist = float('inf')

            for source in myPlanets:
                if source.planet_id() == planet.planet_id():
                    continue
                if source.num_ships() > net_threat:
                    dist = pw.distance(source, planet)
                    if dist < min_dist:
                        min_dist = dist
                        closest_source = source

            if closest_source:
                return closest_source, planet, net_threat + 1  # +1 for safety

    targets = []
    for neut in pw.neutral_planets():
        targets.append((neut, NEUTRAL))
    for enemy in pw.enemy_planets():
        targets.append((enemy, ENEMY))

    if not targets:
        return None, None, 0

    bestMy = myPlanets[0]
    bestN = targets[0][0]
    bestValue = float('inf')
    num_ships = 0

    for myP in myPlanets:
        for (targ, typeP) in targets:
            dist = pw.distance(myP, targ)
            needed = targ.num_ships() + 1
            rate = targ.growth_rate()

            if typeP == ENEMY:
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
            if rate == 0:
                continue
            value = (dist + needed) / rate

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
