from pulp import *


def main():
    zone = int(input('Which zone do you want to model: '
                     '\n 1. Norte '
                     '\n 2. Centro Tulua'
                     '\n 3. Centro Buga '
                     '\n 4. Sur Oriente '
                     '\n 5. Sur Occidente '
                     '\n\nType here: '))
    zone_list = {
        1: 'norte',
        2: 'centro_tulua',
        3: 'centro_buga',
        4: 'sur_oriente',
        5: 'sur_occidente',
    }

    # Empty variables to be assigned later and used on the model
    totals = []
    ubications = []
    tolls = []
    to_save = 0  # We can use this as a mark to check if the file below should be updated
    file = ''

    # File where the zone object is located
    file_path = 'objects/zone_' + zone_list[zone] + '.json'

    # Check if zone file exist
    try:
        file = open(file_path)
        # Do something with the file
    except IOError:
        print('This zone file doesnt exist yet, please create it first.')
        exit()

    zone_object = json.loads(file.read())

    # Loop each city on the object and assign certain values to the empty variables declared before
    for x in zone_object:
        ubications.append(x['city'])
        totals.append(x['distance'])
        if 'tolls' not in x:
            tolls_total = int(input('Tolls total for ' + x['city'] + ': '))
            x['tolls'] = {'total': tolls_total}
            tolls.append(x['tolls']['total'])
            to_save = 1
        else:
            tolls.append(x['tolls']['total'])
    file.close()

    # File should be updated? Let's update it with new values.
    if to_save == 1:
        update_file(zone_object, file_path)

    #
    # This is where the model starts
    #

    # Associate totals with ubications(cities)
    total_distance = makeDict([ubications], totals)

    # Associate tolls with ubications
    total_tolls = makeDict([ubications], tolls)

    # Define a binary variable to determine which city will be used as CD.
    y = LpVariable.dicts("y", ubications, 0, 1, LpBinary)

    # Initializing problem
    prob = LpProblem("planning_problem_of_kits", LpMinimize)

    # Objective Function
    prob += lpSum([y[p] * (total_distance[p] + total_tolls[p]) for p in ubications]), "Costo Total"

    # First constraint, the sum of all "y" must be equals to "1" (one), this mean that only one city will be used as CD.
    prob += lpSum(y) == 1

    # Export problem as LP format
    prob.writeLP("KitsProblem.lp")

    # Solve Problems
    prob.solve()

    # Se imprime el status del problema
    print("Status:", LpStatus[prob.status])
    # Se imprimen las variables
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    # Se imprime la función objetivo
    print("Costo Total = ", value(prob.objective))


def update_file(obj, file_path):
    file = open(file_path, 'w')
    file.write(json.dumps(obj, indent=2, sort_keys=True))
    file.close()


if __name__ == '__main__':
    main()
