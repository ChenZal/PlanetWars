class Fleet:
    def __init__(self, owner, num_ships, source_planet, destination_planet,
                 total_trip_length, turns_remaining):
        self._owner = owner
        self._num_ships = num_ships
        self._source_planet = source_planet
        self._destination_planet = destination_planet
        self._total_trip_length = total_trip_length
        self._turns_remaining = turns_remaining

    def owner(self):
        return self._owner

    def num_ships(self):
        return self._num_ships

    def source_planet(self):
        return self._source_planet

    def destination_planet(self):
        return self._destination_planet

    def total_trip_length(self):
        return self._total_trip_length

    def turns_remaining(self):
        return self._turns_remaining


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
        # Get the earliest enemy arrival time
        enemy_fleets_to_planet = [
            fleet for fleet in enemyFleets if fleet.destination_planet() == planet.planet_id()
        ]
        if not enemy_fleets_to_planet:
            continue

        # Determine latest enemy fleet arrival
        latest_arrival = max(fleet.turns_remaining() for fleet in enemy_fleets_to_planet)

        incoming_enemy_ships = sum(fleet.num_ships() for fleet in enemy_fleets_to_planet)

        # Account for planet's growth until the enemy arrives
        projected_growth = planet.growth_rate() * latest_arrival
        projected_defenders = planet.num_ships() + projected_growth

        if projected_defenders > incoming_enemy_ships:
            continue

        incoming_my_ships = sum(
            fleet.num_ships()
            for fleet in myFleets
            if fleet.destination_planet() == planet.planet_id()
        )

        net_threat = incoming_enemy_ships - (projected_defenders + incoming_my_ships)
        if net_threat > 0:
            closest_source = None
            min_dist = float('inf')

            for source in myPlanets:
                if source.planet_id() == planet.planet_id():
                    continue

                dist = pw.distance(source, planet)
                if source.num_ships() > net_threat + 1 and dist < min_dist:
                    closest_source = source
                    min_dist = dist

            if closest_source:
                return closest_source, planet, net_threat + 1  # +1 for safety

    # offense
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
            if rate != 0:
                value = (0.5 * dist + needed) / rate
            else:
                value = 1000 * 1000 * 1000

            if (value < bestValue) and needed < myP.num_ships():
                bestValue = value
                bestMy = myP
                bestN = targ
                num_ships = needed

    return bestMy, bestN, num_ships


def issue_order(pw, source_planet, destination_planet, num_ships):
    if isinstance(source_planet, int):
        source_planet_id = source_planet
        source = pw._planets[source_planet_id]
    else:
        source_planet_id = source_planet.planet_id()
        source = source_planet

    if isinstance(destination_planet, int):
        destination_planet_id = destination_planet
    else:
        destination_planet_id = destination_planet.planet_id()

    # Immediately update source planet's ship count
    source.remove_ships(num_ships)

    # Calculate distance
    distance = pw.distance(source_planet_id, destination_planet_id)

    # Create and track the fleet
    new_fleet = Fleet(1, num_ships, source_planet_id, destination_planet_id, distance, distance)
    pw._fleets.append(new_fleet)

    # Store the command for output later
    return source_planet_id, destination_planet_id, num_ships


def do_turn(pw):
    if len(pw.my_planets()) == 0:
        return
    if len(pw.enemy_planets()) == 0:
        return

    orders = []
    while True:
        myBest, targetBest, num_ships = choose_closet_possible(pw)
        if myBest is None or num_ships == 0:
            break
        if myBest not in pw.my_planets():
            break
        if myBest.planet_id() not in [p.planet_id() for p in pw.my_planets()]:
            break
        if myBest.num_ships() < num_ships:
            break
        orders.append(issue_order(pw, myBest, targetBest, num_ships))

    for order in orders:
        pw.issue_order(order[0], order[1], order[2])
