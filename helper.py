def choose_closet_possible(pw):
    myPlanets = pw.my_planets()
    isNeut = True
    targets = []
    if len(pw.neutral_planets()) != 0:
        targets = pw.neutral_planets()
    else:
        targets = pw.enemy_planets()
        isNeut = False

    bestMy = myPlanets[0]
    bestN = targets[0]
    bestDist = 10000000
    num_ships = 0

    for myP in myPlanets:
        for n in targets:
            dist = pw.distance(myP, n)
            needed = n.num_ships()
            if not isNeut:
                pass
            if (dist < bestDist) and needed < myP.num_ships():
                bestDist = dist
                bestMy = myP
                bestN = n
                num_ships = needed

    return (bestMy, bestN, num_ships)
