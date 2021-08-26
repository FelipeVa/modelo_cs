#FUENTE: ASOCIO 2021, TALLER PULP - Andrés Felipe Osorio Muriel, Ph.D.
# Se importa la librería
from pulp import *

# Creamos una lista con las posibles ubicaciones de las plantas
Plantas = {"San Francisco",
          "Los Angeles",
          "Phoenix",
          "Denver"}

# Definimos la capacidad de las plantas usando un diccionario
Capacidad = {
          "San Francisco":1700,
          "Los Angeles"  :2000,
          "Phoenix"      :1700,
          "Denver"       :2000
          }

# Definimos el costo fijo de las plantas usando un diccionario
CostoFijo = {
          "San Francisco":70000,
          "Los Angeles"  :70000,
          "Phoenix"      :65000,
          "Denver"       :70000
          }

# Creamos la lista de tiendas o puntos de demanda
Tiendas = ["San Diego",
          "Barstow",
          "Tucson",
          "Dallas"]

# Creates a dictionary for the number of units of demand at each store
Demanda = {
          "San Diego":1700,
          "Barstow"  :1000,
          "Tucson"   :1500,
          "Dallas"   :1200
          }

# Se crea una lista de los costos de transporte
CostosTransporte = [  #Stores
         #SD BA TU DA
         [5, 3, 2, 6], #SF
         [4, 7, 8, 10],#LA    Plants
         [6, 5, 3, 8], #PH
         [9, 8, 6, 5]  #DE         
         ]

# Se convierte la lista anterior en un diccionario asociandolo a las plantas y tiendas 
costo_transporte = makeDict([Plantas,Tiendas],CostosTransporte,0)

# Se define la variable de decisión x que representa el flujo entre plantas y tiendas
x = LpVariable.dicts("x",(Plantas,Tiendas),0,None,LpContinuous)

# Se define la variable binaria de si se construye una planta o no
y = LpVariable.dicts("y",(Plantas),0,1,LpInteger)

# Se crea el problema 
prob = LpProblem("Computer Plant Problem",LpMinimize)

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