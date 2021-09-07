from pulp import *
from common import file_selector, file_loader, get_object_from_file


def main():
    instance = file_selector()
    zone = instance['file']
    zone_list = instance['file_list']
    zone_object = file_loader(zone, zone_list)
    collection_center_object = get_object_from_file('collection_center')
    kits_object = get_object_from_file('results/kits_result')

    collection_center = 0
    vehicle_max_capacity = 8000
    weight_of_kit = 22
    fixed_cost = 342
    capacity = 0

    # Empty variables to be assigned later and used on the model
    totals = []
    ubications = []
    tolls = {}
    kits = {}

    # Loop each city on the object and assign certain values to the empty variables declared before
    for x in zone_object:
        total_tolls = 0
        ubications.append(x['city'])
        totals.append(x['distance'])
        kits[x['city']] = kits_object[x['city']]
        capacity += kits_object[x['city']]

        for i in x['tolls']:
            total_tolls += i
            tolls[x['city']] = total_tolls

    for z in collection_center_object[zone_list[zone]]:
        collection_center += z

    # # # # # # # # # # # # # # # # # #
    # This is where the model starts  #
    # # # # # # # # # # # # # # # # # #

    # Associate totals with ubications(cities)
    total_distance = makeDict([ubications], totals)

    # Define a binary variable to determine which city will be used as CD.
    y = LpVariable.dicts("y", ubications, 0, 1, LpBinary)

    # Initializing problem
    prob = LpProblem("planning_problem_of_kits", LpMinimize)

    # Objective Function
    prob += lpSum([y[p] * ((total_distance[p] * fixed_cost * kits[p] * weight_of_kit) + (
            (tolls[p] + collection_center) * ((kits[p] * weight_of_kit) / vehicle_max_capacity))) for p in ubications]), "Costo Total"

    # First constraint, the sum of all "y" must be equals to "1" (one), this mean that only one city will be used as CD.
    prob += lpSum(y) == 1

    prob += lpSum(kits[p] for p in ubications) <= capacity


    # Export problem as LP format
    prob.writeLP("KitsProblem.lp")

    # Solve Problems
    prob.solve(PULP_CBC_CMD(gapRel=0))

    # Se imprime el status del problema
    print("Status:", LpStatus[prob.status])

    # Se imprimen las variables
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    # Se imprime la función objetivo
    print("Costo Total = ", value(prob.objective))


if __name__ == '__main__':
    main()
