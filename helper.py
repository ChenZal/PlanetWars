def choose_closet_possible(pw):
    myPlanets = pw.my_planets()
    isNeut = True
    if len(pw.neutral_planets()) != 0:
        targets = pw.neutral_planets()
    else:
        targets = pw.enemy_planets()
        isNeut = False

    bestMy = None
    bestN = None
    bestDist = 10000000
    num_ships = 0

    for myP in myPlanets:
        for n in targets:
            dist = pw.distance(bestMy, bestN)
            needed = n.num_ships()
            if not isNeut:
                pass

            if (dist < bestDist) and needed < myP.num_ships():
                bestDist = dist
                bestMy = myPlanets
                bestN = n
                num_ships = needed

    return (bestMy, bestN, num_ships)
