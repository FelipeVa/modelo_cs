# Se importa la librería
from pulp import *

# conjuntos:


# creamos la ubicación del centro de acopio
centro_acopio = {"aeropuerto"}

# Creamos una lista con las posibles ubicaciones para los centros de distribución
CDIS_soc = {"cali", "yumbo", "jamundi", "vijes", "la_cumbre", "dagua"}

# Creamos la lista de tiendas o puntos de demanda
zonas_afectadas_soc = {"cali", "yumbo", "jamundi", "vijes", "la_cumbre", "dagua"}

# Parametros:


# peso por cada kit alimenticio (kg)
P = 22
# capacidad máxima de cada vehículo(kg)
CV = 8000
# definimos la capacidad del centro de acopio
cap = 30361

# Creates a dictionary for the number of units of demand at each store
Demanda_soc = {"cali": 6778, "yumbo": 5498, "jamundi": 1488, "vijes": 5742, "la_cumbre": 4646, "dagua": 6209}

# Se crea una lista de los costos de transporte
costostransporte = [
    [7944, 4553, 13722, 9169, 11587, 20850]
]

costos_transp = [
    [0, 5118, 6060, 11587, 12152, 16108],
    [4804, 0, 10770, 7222, 7787, 18306],
    [5997, 10959, 0, 17458, 17992, 22388],
    [11492, 7002, 18243, 0, 10927, 27663],
    [12215, 7724, 18777, 11021, 0, 11053],
    [16140, 18840, 22168, 27381, 11147, 0],
]

peajes1 = [
    [0, 10900, 0, 10900, 10900, 0]
]

peajes2 = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 10900],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 10900, 0, 0],
]

# Se convierte la lista anterior en un diccionario asociandolo al centro de acopio a CDIS
costo_transporte1 = makeDict([centro_acopio, CDIS_soc], costostransporte, 0)
# Se convierte la lista anterior en un diccionario asociandolo a los CDIS y las zonas afectadas
costo_transporte2 = makeDict([CDIS_soc, zonas_afectadas_soc], costos_transp, 0)
# se crea el diccionario de los costos de los peajes entre el centro de acopio y los CDIS
peajes_ij = makeDict([centro_acopio, CDIS_soc], peajes1, 0)
# se crea el diccionario de los costos de los peajes entre los CDIS y las zonas afectadas
peajes_jk = makeDict([CDIS_soc, zonas_afectadas_soc], peajes2, 0)

print(peajes_ij)
# Variables de decisión:

# Se define la variable de decisión X1 que representa la cantidad de kits alimenticios a enviar desde el centro de acopio i a los CDIS j
X1 = LpVariable.dicts("X1", (centro_acopio, CDIS_soc), 0, None, LpInteger)
# Se define la variable de decisión X2 que representa la cantidad de kits alimenticios a enviar desde los CDIS j a cada zona afectada
X2 = LpVariable.dicts("X2", (CDIS_soc, zonas_afectadas_soc), 0, None, LpInteger)
# Se define la variable de decisión V1 que representa la cantidad de viajes a realizar desde el centro de acopio “i” a cada centro de distribución “j”
V1 = LpVariable.dicts("V1", (centro_acopio, CDIS_soc), 0, None, LpInteger)
# Se define la variable de decisión V2 que representa la cantidad de viajes a realizar desde el centro de distribución a las zonas afectadas.
V2 = LpVariable.dicts("V2", (CDIS_soc, zonas_afectadas_soc), 0, None, LpInteger)
# Se define la variable binaria de si se abre o no un centro de distribución
W = LpVariable.dicts("W", (CDIS_soc), 0, 1, LpBinary)

# total_distance = makeDict([ubications], totals)

M = cap

# print(M)

# Función objetivo:

# Se crea el problema
problema = LpProblem("problema_de_logistica_humanitaria", LpMinimize)

# Se agrega la función objetivo (la única diferencia es que esta ecuación no tiene lado derecho)
problema += lpSum([[X1[i][j] * costo_transporte1[i][j] for i in centro_acopio] for j in CDIS_soc]) + lpSum(
    [[V1[i][j] * peajes_ij[i][j] for i in centro_acopio] for j in CDIS_soc]) + lpSum(
    [[X2[j][k] * costo_transporte2[j][k] for j in CDIS_soc] for k in zonas_afectadas_soc]) + lpSum(
    [[V2[j][k] * peajes_jk[j][k] for j in CDIS_soc] for k in zonas_afectadas_soc])

# Restricciones:

# Oferta:
for i in centro_acopio:
    problema += lpSum([X1[i][j] for j in CDIS_soc]) <= cap

# Apertura de CDIS:
for j in CDIS_soc:
    problema += lpSum([X1[i][j] for i in centro_acopio]) <= M * W[j]

# Apertura de CDIS:
for j in CDIS_soc:
    problema += lpSum([X2[j][k] for k in zonas_afectadas_soc]) <= M * W[j]

# Cantidad de CDIS a abrir por zona:
problema += lpSum([W[j] for j in CDIS_soc]) <= 1

# Demanda:
for k in zonas_afectadas_soc:
    problema += lpSum([X2[j][k] for j in CDIS_soc]) >= Demanda_soc[k]

# Transbordo
for j in CDIS_soc:
    problema += lpSum([X1[i][j]] for i in centro_acopio) - lpSum([X2[j][k]] for k in zonas_afectadas_soc) == 0

# Transporte:
for i in centro_acopio:
    for j in CDIS_soc:
        problema += [V1[i][j]] >= ((X1[i][j] * P) / CV)

for j in CDIS_soc:
    for k in zonas_afectadas_soc:
        problema += [V2[j][k]] >= ((X2[j][k] * P) / CV)

# Se exporta el problema a un formato .lp
# problema.writeLP("problema_de_logistica_humanitaria")

# Se resuelve el problema usando el solver por defecto (CBC)
# problema.solve()
problema.solve(PULP_CBC_CMD(fracGap=0))

# Se imprime el status del problema
print("Status:", LpStatus[problema.status])

# Se imprimen las variables
for v in problema.variables():
    if (v.varValue != 0):
        print(v.name, "=", v.varValue)

# Se imprime la función objetivo
print("Costo Total de transporte= ", value(problema.objective))