
import time
import math
import matplotlib.pyplot as plt
from funciones import carga, aproximacion1, aproximacion2, backtracking

FACTOR=1

def medir_tiempo(funcion, maestros, num_grupos,grupos,result_Greedy,suma_Greedy):
    inicio = time.time()
    if funcion.__name__ == 'backtracking':
        resultado, suma = backtracking(maestros, 0, grupos, result_Greedy, suma_Greedy, num_grupos, set())
    else:
        resultado = funcion(maestros, num_grupos)
    fin = time.time()
    return fin - inicio


archivo = input("Ingrese nombre del archivo: ")
grupos, maestros = carga(archivo)
    
num_grupos = len(grupos)
n = len(maestros)
tiempos_aprox1 = []
tiempos_aprox2 = []
tiempos_backtracking = []

for i in range(1, n + 1):
	result_aprox1 = aproximacion1(maestros[:i], len(grupos))
	suma_aprox1 = sum(tot * tot for _, tot in result_aprox1)

	#tiempo_aprox1 = medir_tiempo(aproximacion1, maestros[:i], num_grupos,grupos,0,0)
	#tiempo_aprox2 = medir_tiempo(aproximacion2, maestros[:i], num_grupos,grupos,0,0)
	tiempo_backtracking = medir_tiempo(backtracking, maestros[:i], num_grupos,grupos,result_aprox1,suma_aprox1)
	
	#tiempos_aprox1.append(tiempo_aprox1)
	#tiempos_aprox2.append(tiempo_aprox2)
	tiempos_backtracking.append(tiempo_backtracking)
		
#Graficar los tiempos de ejecución  
escala = 10**6 * FACTOR
tiempos_aprox1_escalados = [t * escala for t in tiempos_aprox1]
tiempos_aprox2_escalados = [t * escala for t in tiempos_aprox2]
tiempos_backtracking_escalados = [t * escala for t in tiempos_backtracking]

# Complejidad teórica para comparación
dos_a_la_n = [2 ** i for i in range(1, n + 1)]
#complejidad_aproximacion1 = [(i*num_grupos + i * math.log(i)) for i in range(1, n + 1)]
#complejidad_aproximacion2 = [(i * math.log(i)) for i in range(1, n + 1)]


plt.figure(figsize=(12, 8))
#plt.plot(range(1, n + 1), tiempos_aprox1_escalados, marker='o', label='sol_aprox1')
#plt.plot(range(1, n + 1), tiempos_aprox2_escalados, marker='x', label='sol_Greedy2')
plt.plot(range(1, n + 1), tiempos_backtracking_escalados, marker='s', label='backtracking')
#plt.plot(range(1, n + 1), complejidad_aproximacion1, linestyle='--', label='O(n*k + n * log(n))')
#plt.plot(range(1, n + 1), complejidad_aproximacion2, linestyle='--', label='O(n * log(n))')
plt.plot(range(1, n + 1), dos_a_la_n, linestyle='--', label='O(2^n)')

plt.xlabel('Número de maestros')
plt.ylabel('Tiempo de ejecución (escalado)')
plt.title('Tiempo de ejecución de los algoritmos')
plt.legend()
plt.grid(True)
plt.show()
