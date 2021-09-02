from pulp import *
from common import file_selector, file_loader, get_object_from_file


def main():
    collection_center = {'aeropuerto': 200000}
    vehicle_max_capacity = 8000
    weight_of_kit = 22

    instance = file_selector()
    zone = instance['file']
    zone_list = instance['file_list']
    zone_object = file_loader(zone, zone_list)
    kits_object = get_object_from_file('results/kits_result')

    # Empty variables to be assigned later and used on the model
    totals = []
    ubications = []
    tolls = []
    kits = {}

    # Loop each city on the object and assign certain values to the empty variables declared before
    for x in zone_object:
        if 'tolls' in x:
            continue

        ubications.append(x['city'])
        totals.append(x['distance'])
        kits[x['city']] = kits_object[x['city']]
    # # # # # # # # # # # # # # # # # #
    # This is where the model starts  #
    # # # # # # # # # # # # # # # # # #

    # Associate totals with ubications(cities)
    total_distance = makeDict([ubications], totals)

    # Associate tolls with ubications
    total_tolls = makeDict([ubications], tolls)

    # Define a binary variable to determine which city will be used as CD.
    y = LpVariable.dicts("y", ubications, 0, 1, LpBinary)

    # Initializing problem
    prob = LpProblem("planning_problem_of_kits", LpMinimize)

    # Objective Function
    prob += lpSum([y[p] * (total_distance[p]) for p in ubications]), "Costo Total"

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


if __name__ == '__main__':
    main()
