#FUENTE: ASOCIO 2021, TALLER PULP - Andrés Felipe Osorio Muriel, Ph.D.
# Se importa la librería
from pulp import *

# Creamos una lista con las posibles ubicaciones de las plantas
Ubications = {
  "Aeropuerto",
  "Palmira",
  "Candelaria",
  "El Cerrito",
  "Florida",
  "Pradera",
}

# Definimos la capacidad de las plantas usando un diccionario
Capacidad = {
"San Francisco":1700,
"Los Angeles"  :2000,
"Phoenix"      :1700,
"Denver"       :2000
}

# Definimos el costo fijo de las plantas usando un diccionario
Tolls = {
  "Palmira"     :0,
  "Candelaria"  :0,
  "El Cerrito"  :0,
  "Florida"     :0,
  "Pradera"     :0
}

# Creamos la lista de tiendas o puntos de demanda
Tiendas = ["San Diego",
          "Barstow",
          "Tucson",
          "Dallas"]

# Creates a dictionary for the number of units of demand at each store
Demand = {
"Palmira"     :272.69  ,
"Candelaria"  :218.394 ,
"El Cerrito"  :121     ,
"Florida"     :231.682 ,
"Pradera"     :14.234
}


# Se crea una lista de los costos de transporte
DistanceMatriz = [  #Stores
  #PA    #CA   #EL   #FL   #PR   #A
  [0,    19.5, 26.7, 32.4, 18.9, 14.8], #PA  D[0][i] 
  [18.8, 0,    35.4, 18,   14.2, 23.9], #CA  D[1][i]      
  [26.7, 34.6, 0,    53,   43.9, 32.5], #EL  D[2][i]      
  [32.8, 18.6, 53.6, 0,    14.3, 53.8], #FL  D[3][i]    PLANTAS
  [18.7, 14,   43.3, 14.1, 0,    38], #PR    D[4][i]    
  [15.6, 23.9, 32.5, 53.8, 38,    0], #A      D[5][i]  
]  

# Se convierte la lista anterior en un diccionario asociandolo a las plantas y tiendas 
total_distance = makeDict([Ubications, Ubications], DistanceMatriz, 0)

# x Se define la variable binaria de si se construye una planta o no
x = LpVariable.dicts("x",(Ubications), 0, 1, LpInteger)

# Se define la variable de decisión x que representa el flujo entre plantas y tiendas
y = LpVariable.dicts("y", (Plantas,Tiendas), 0, None, LpContinuous)

# Se crea el problema 
prob = LpProblem("planning problem of kits", LpMinimize)

# Se agrega la función objetivo (la única diferencia es que esta ecuación no tiene lado derecho)
prob += lpSum([[x[p][s]*costo_transporte[p][s] for p in Plantas] for s in Tiendas])+lpSum([CostoFijo[p]*y[p] for p in Plantas]),"Costo Total"

# El flujo despachado de cada planta no debe superar su capacidad(en caso de que se abra)
for p in Plantas:
    prob += lpSum([x[p][s] for s in Tiendas])<=Capacidad[p]*y[p], "Sum of Products out of Plant %s"%p

# LA demanda de cada cliente debe ser satisfecha
for s in Tiendas:
    prob += lpSum([x[p][s] for p in Plantas])>=Demanda[s], "Sum of Products into Stores %s"%s

# Se exporta el problema a un formato .lp
prob.writeLP("ComputerPlantProblem.lp")

# Se resuelve el problema usando el solver por defecto (CBC)
prob.solve()

# Se imprime el status del problema
print("Status:", LpStatus[prob.status])

# Se imprimen las variables
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Se imprime la función objetivo    
print("Costo Total = ", value(prob.objective))