from pulp import *

zone = input('Which zone do you want to open: ')

file = open('objects/zone_' + zone.replace(' ', '_') + '.text')
zone_object = json.loads(file.read())
totals = []
ubications = []

for x in zone_object:
    ubications.append(x['city'])
    totals.append(x['distance'])
file.close()

# # Se convierte la lista anterior en un diccionario asociandolo a las plantas y tiendas
total_distance = makeDict([ubications], totals)

# print(total_distance)

# # Se define la variable de decisión x que representa el flujo entre plantas y tiendas
# x = LpVariable.dicts("x", (ubications, totals), 0, None, LpContinuous)

# x Se define la variable binaria de si se construye una planta o no
y = LpVariable.dicts("y", ubications, 0, 1, LpBinary)

# # Se crea el problema
prob = LpProblem("planning_problem_of_kits", LpMinimize)

# Se agrega la función objetivo (la única diferencia es que esta ecuación no tiene lado derecho)
prob += lpSum([y[p] * total_distance[p] for p in ubications]), "Costo Total"

# rob += lpSum([x[p] * total_distance[p] for p in ubications]) + lpSum(
#     [CostoFijo[p] * y[p] for p in Plantas]), "Costo Total"
#
# # El flujo despachado de cada planta no debe superar su capacidad(en caso de que se abra)
# for p in Plantas:
#     prob += lpSum([x[p][s] for s in Tiendas]) <= Capacidad[p] * y[p], "Sum of Products out of Plant %s" % p
# El flujo despachado de cada planta no debe superar su capacidad(en caso de que se abra)
prob += lpSum(y) == 1
# for p in ubications:
#     prob += lpSum([y[p]]) <= 1 or 0, "Sum of Products into Stores %s" % p
#     prob += lpSum([y[p]]) <= 1 or 0, "Sum of Products into Stores %s" % p
#
# # LA demanda de cada cliente debe ser satisfecha
# for s in Tiendas:
#     prob += lpSum([x[p][s] for p in Plantas]) >= Demanda[s], "Sum of Products into Stores %s" % s
#
# # Se exporta el problema a un formato .lp
prob.writeLP("ComputerPlantProblem.lp")
#
# # Se resuelve el problema usando el solver por defecto (CBC)
prob.solve()
#
# # Se imprime el status del problema
print("Status:", LpStatus[prob.status])
#
# # Se imprimen las variables
for v in prob.variables():
    print(v.name, "=", v.varValue)
#
# # Se imprime la función objetivo
print("Costo Total = ", value(prob.objective))
