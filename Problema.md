Un problema de ubicación de instalaciones
================================================
La empresa Cosmic Computer que desea establecer una producción en Estados Unidos. Están contemplando la construcción de plantas de producción en hasta 4 ubicaciones. Cada ubicación tiene restricciones de planificación que determinan efectivamente la producción mensual posible en cada ubicación. Los costos fijos mensuales de las diferentes ubicaciones han sido calculados por el departamento de contabilidad y se enumeran a continuación, junto con la cantidad que cada fábrica puede suministrar::

|Ubicación	|Capacidad	|Costo Fijo|
| ------------- | ------------- |
|San Francisco	| 1700	| 70000
|Los Angeles	|2000	|70000|
|Phoenix	|1700	|65000|
|Denver	|2000	|70000|

Estas plantas abastecerán a tiendas en 4 ubicaciones. La demanda prevista y los costos de transporte por unidad para el suministro de las 4 plantas de producción a las 4 tiendas se muestran a continuación:


![Image text](images/cosmic_network.jpg)

Demanda
----
|Tienda	|Demanda|
| ------------- | ------------- |
|San Diego	|1700|
|Barstow	|2000|
|Tucson	|1700|
|Dallas	|2000|


Costos de transporte
---
||San Diego	|Barstow	|Tucson	|Dallas|
| ------------- | ------------- |
|San Francisco|	5	|3	|2	|6|
|Los Angeles	|4	|7	|8	|10|
|Phoenix	|6	|5	|3	|8|
|Denver	|9	|8	|6	|5|

https://twiki.esc.auckland.ac.nz/do/view/OpsRes/CosmicComputersSolverStudio#tasks

¿Dónde debería instalar la empresa sus plantas para minimizar sus costos totales (fijo más transporte)?

Fuente: ASOCIO 2021, TALLER PULP - Andrés Felipe Osorio Muriel, Ph.D.


Formulación del problema

![Image text](images/modelo.png)