from pulp import *
from common import file_selector, file_loader, create_result_json_file, create_json_file


def main():
    instance = file_selector()
    zone = instance['file']
    zone_list = instance['file_list']
    zone_object = file_loader(zone, zone_list)
    cap_kits = 200000
    result = {}

    # Empty variables to be assigned later and used on the model
    ubications = []
    demand = {}

    # Loop each city on the object and assign certain values to the empty variables declared before
    for x in zone_object:
        ubications.append(x['city'])
        demand[x['city']] = x['kits']

    # Variables de decision

    # Variable de porcentaje de asignación de ayudas
    y = LpVariable("porcentaje_asignacion", 0, None, LpContinuous)
    # flujo entre centro de acopio y CD
    x = LpVariable.dicts("kits_asignados", ubications, 0, None, LpInteger)

    # Creacion del problema
    model = LpProblem("problema_de_asignacion_de_kits", LpMaximize)

    # Funcion Objetivo
    model += y

    # Proporcion de ayudas asignadas en cada municipio
    for i in ubications:
        model += lpSum(x[i] * (1 / demand[i])) >= y

    model += lpSum([x[i] for i in ubications]) <= cap_kits

    # Solve the problem
    model.solve()

    # Se imprimen las variables, también se podrían guardar en listas y usarlas para calculos adicionales
    for v in model.variables():
        if v.name == 'porcentaje_asignacion':
            result['result'] = v.varValue
            continue

        result[v.name.replace('kits_asignados_', '')] = v.varValue

        print(v.name, "=", v.varValue)

    create_result_json_file(result, 'kits_result')

    # Se imprime la funciónobjetivo
    print("funcion_objetivo", value(model.objective))


if __name__ == '__main__':
    main()
