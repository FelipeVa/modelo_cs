# Se importa la librería
from pulp import *

# conjuntos:


# creamos la ubicación del centro de acopio
centro_acopio = {"aeropuerto"}

# Creamos una lista con las posibles ubicaciones para los centros de distribución
CDIS_ct = {"tulua", "andalucia", "bugalagrande", "trujillo", "riofrio", "caicedonia", "sevilla", "san_pedro",
           "roldanillo", "bolivar", "el_dovio"}

# Creamos la lista de tiendas o puntos de demanda
zonas_afectadas_ct = {"tuluá", "andalucía", "bugalagrande", "trujillo", "riofrío", "caicedonia", "sevilla", "san_pedro",
                      "roldanillo", "bolívar", "el_dovio"}

# Parametros:


# peso por cada kit alimenticio (kg)
P = 22
# capacidad máxima de cada vehículo(kg)
CV = 8000
# definimos la capacidad del centro de acopio
cap = 400000
centro_acopio = {"aeropuerto": 400000}
# Creates a dictionary for the number of units of demand at each store
Demanda_ct = {"tuluá": 1511, "andalucía": 1651, "bugalagrande": 9437, "trujillo": 5246, "riofrío": 2884,
              "caicedonia": 8588, "sevilla": 3616, "san_pedro": 11146, "roldanillo": 7784, "bolívar": 6934,
              "el_dovio": 5360}

# Se crea una lista de los costos de transporte
costostransporte = [
    [24398, 27695, 29547, 31714, 28700, 47100, 41134, 20724, 40506, 42704, 47728]
]

costos_transp = [
    [0, 3454, 5401, 8007, 4836, 22859, 17113, 4082, 16799, 13565, 28040]
    [3454, 0, 1821, 11398, 8227, 19280, 13533, 7442, 21258, 16956, 18275]
    [5401, 1821, 0, 13062, 9891, 17835, 12120, 9137, 19813, 18620, 23048]
    [8007, 11398, 13062, 0, 3014, 30395, 24680, 11178, 15857, 12591, 22765]
    [4836, 8227, 9891, 3014, 0, 27381, 21635, 8164, 12811, 9577, 19751]
    [22859, 19280, 17835, 30395, 27381, 0, 6343, 26721, 26564, 30050, 29799]
    [17113, 13533, 12120, 24680, 21635, 6343, 0, 30552, 27067, 30552, 30301]
    [4082, 7442, 9137, 11178, 8164, 26721, 30552, 0, 20190, 16956, 31714]
    [16799, 21258, 19813, 15857, 12811, 26564, 27067, 20190, 0, 3737, 7159]
    [13565, 16956, 18620, 12591, 9577, 30050, 30552, 16956, 3737, 0, 10676]
    [28040, 18275, 23048, 22765, 19751, 29799, 30301, 31714, 7159, 10676, 0]
]

peajes1 = [
    [21700, 21700, 21700, 21700, 21700, 44700, 32500, 21700, 21700, 21700, 21700]
]

peajes2 = [
    [0, 0, 0, 0, 0, 23000, 10800, 0, 10800, 10800, 10800]
    [0, 0, 0, 0, 0, 23000, 10800, 0, 10800, 10800, 10800]
    [0, 0, 0, 0, 0, 23000, 10800, 0, 10800, 10800, 10800]
    [0, 0, 0, 0, 0, 23000, 10800, 0, 10800, 10800, 10800]
    [0, 0, 0, 0, 0, 23000, 10800, 0, 10800, 10800, 10800]
    [23000, 23000, 23000, 23000, 23000, 0, 0, 23000, 12200, 12200, 12200]
    [10800, 10800, 10800, 10800, 10800, 0, 0, 10800, 10800, 10800, 10800]
    [0, 0, 0, 0, 0, 23000, 10800, 0, 10800, 10800, 10800]
    [10800, 10800, 10800, 10800, 10800, 12200, 10800, 10800, 0, 0, 0]
    [10800, 10800, 10800, 10800, 10800, 12200, 10800, 10800, 0, 0, 0]
    [10800, 10800, 10800, 10800, 10800, 12200, 10800, 10800, 0, 0, 0]
]

# Se convierte la lista anterior en un diccionario asociandolo al centro de acopio a CDIS
costo_transporte1 = makeDict([centro_acopio, CDIS_ct], costostransporte, 0)
# Se convierte la lista anterior en un diccionario asociandolo a los CDIS y las zonas afectadas
costo_transporte2 = makeDict([CDIS_ct, zonas_afectadas_ct], costos_transp, 0)
# se crea el diccionario de los costos de los peajes entre el centro de acopio y los CDIS
peajes_ij = makeDict([centro_acopio, CDIS_ct], peajes1, 0)
# se crea el diccionario de los costos de los peajes entre los CDIS y las zonas afectadas
peajes_jk = makeDict([CDIS_ct, zonas_afectadas_ct], peajes2, 0)

# Variables de decisión:

# Se define la variable de decisión X1 que representa la cantidad de kits alimenticios a enviar desde el centro de acopio i a los CDIS j
X1 = LpVariable.dicts("X1", (centro_acopio, CDIS_ct), 0, None, LpInteger)
# Se define la variable de decisión X2 que representa la cantidad de kits alimenticios a enviar desde los CDIS j a cada zona afectada
X2 = LpVariable.dicts("X2", (CDIS_ct, zonas_afectadas_ct), 0, None, LpInteger)
# Se define la variable de decisión V1 que representa la cantidad de viajes a realizar desde el centro de acopio “i” a cada centro de distribución “j”
V1 = LpVariable.dicts("V1", (centro_acopio, CDIS_ct), 0, None, LpInteger)
# Se define la variable de decisión V2 que representa la cantidad de viajes a realizar desde el centro de distribución a las zonas afectadas.
V2 = LpVariable.dicts("V2", (CDIS_ct, zonas_afectadas_ct), 0, None, LpInteger)
# Se define la variable binaria de si se abre o no un centro de distribución
W = LpVariable.dicts("W", (CDIS_ct), 0, 1, LpBinary)

# Función objetivo:

# Se crea el problema
problema = LpProblem("problema_de_logistica_humanitaria", LpMinimize)

# Se agrega la función objetivo (la única diferencia es que esta ecuación no tiene lado derecho)
problema += lpSum([[X1[i][j] * costo_transporte1[i][j] for i in centro_acopio] for j in CDIS_ct]) + lpSum(
    [[V1[i][j] * peajes_ij[i][j] for i in centro_acopio] for j in CDIS_ct]) + lpSum(
    [[X2[j][k] * costo_transporte2[j][k] for j in CDIS_ct] for k in zonas_afectadas_ct]) + lpSum(
    [[V2[j][k] * peajes_jk[j][k] for j in CDIS_ct] for k in zonas_afectadas_ct])

# Restricciones:
# Oferta:
for i in centro_acopio:
    problema += lpSum(
        [X1[i][j] for j in CDIS_ct]) <= cap, "suma de kits de alimentación que salen del centro de acopio %j" % i
# Apertura de CDIS:
for j in CDIS_ct:
    problema += lpSum([X1[i][j] for i in centro_acopio]) <= M * W[j], "se abre o no un centro de distribución %i" % j
for k in zonas_afectadas_ct:
    problema += lpSum([X2[j][k] for j in CDIS_ct]) == M, "valor que toma M %j" % k
    # Cantidad de CDIS a abrir por zona:
    problema += lpSum([W[j] for j in CDIS_ct]) <= 1, "cantidad de CDIS a abrir en %j" % k
# Demanda:
for k in zonas_afectadas_ct:
    problema += lpSum([X2[j][k] for j in CDIS_ct]) >= Demanda_ct[k], "cantidad de CDIS a abrir en %j" % k

# Transporte:
for i in centro_acopio:
    for j in CDIS_ct:
        problema += [V1[i][j] >= ((X1[i][j] * P) / CV),
                     "cantidad de viajes a realizar entre el centro de acopio y los centros de distribución"

        for j in CDIS_ct:
            for
        k in zonas_afectadas_ct:
        problema += [V2[j][k]] >= ((X2[j][
                                        k] * P) / CV), "cantidad de viajes a realizar entre el centro de acopio y los centros de distribución"

        # Se exporta el problema a un formato .lp
        # problema.writeLP("problema_de_logistica_humanitaria")

        # Se resuelve el problema usando el solver por defecto (CBC)
        problema.solve()

        # Se imprime el status del problema
        print("Status:", LpStatus[prob.status])

        # Se imprimen las variables
        for v in problema.variables():
            print(v.name, "=", v.varValue)

        # Se imprime la función objetivo
        print("Costo Total de transporte= ", value(problema.objective))