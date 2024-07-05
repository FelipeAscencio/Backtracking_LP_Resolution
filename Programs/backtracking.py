PRIMER_RENGLON = 2

#recibe el nombre del archivo y devuelve una lista de tuplas de (maestro, poder) y una lista de listas vacias (grupos)
def carga(archivo):
    try:
        nombre_archivo = archivo + ".txt"
        with open(nombre_archivo) as archivo:
            lineas = archivo.readlines()
            num_grupos = int(lineas[1].strip())
            grupos = [([], 0)] * num_grupos
            maestros = []
            for linea in lineas[PRIMER_RENGLON:]:
                datos = linea.strip().split(",")
                maestros.append((datos[0], int(datos[1])))
        return grupos, maestros
    except IOError:
        print("Error al abrir el archivo")
        return None

#recibe la lista de maestros y el numero de grupos, devuelve la lista de los grupos resuelta de forma greedy
def sol_Greedy(maestros, num_grupos):
    maestros_ordenados = sorted(maestros, key=lambda x: x[1], reverse=True)
    resultado = [([], 0)] * num_grupos
    for i in range(len(maestros_ordenados)):
        guerrero, poder = maestros_ordenados[i]
        indice_min = min(range(len(resultado)), key=lambda i: resultado[i][1])
        guerreros, sumatoria = resultado[indice_min]
        resultado[indice_min] = (guerreros + [guerrero], sumatoria + poder)
    return resultado


#recibe el indicel maestro actual y verifica que haya suficientes maestros para que ningun grupo quede vacio
def suficientes_guerreros(grupos, actual, total_guerreros):
    vacios = 0
    for i in range(len(grupos)):
        guerreros, _ = grupos[i]
        if len(guerreros) < 1:
            vacios += 1
    if vacios > total_guerreros - actual:
        return False
    return True

#Resuelve el problema por backtracking, sus podas son: si la solucion actual es peor que la mejor, si no se llega a completar los grupos y si una permutacion de la solucion actual ya fue analizada.
def backtracking(maestros, actual, grupos, mejor_result, mejor_suma, cant_grupos, ya_analizado):
    suma_actual = sum(tot * tot for _, tot in grupos)

    if suma_actual >= mejor_suma or not suficientes_guerreros(grupos, actual, len(maestros)):
        return mejor_result, mejor_suma

    permutacion = tuple(sorted(grupo[1] for grupo in grupos))
    if permutacion in ya_analizado:
        return mejor_result, mejor_suma
    ya_analizado.add(permutacion)

    if actual == len(maestros):
        return [grupo for grupo in grupos], suma_actual

    guerrero, poder = maestros[actual]
    for i in range(cant_grupos):
        guerreros, sumatoria = grupos[i]
        grupos[i] = (guerreros + [guerrero], sumatoria + poder)

        mejor_result, mejor_suma = backtracking(maestros, actual + 1, grupos, mejor_result, mejor_suma, cant_grupos, ya_analizado)

        grupos[i] = (guerreros, sumatoria)
    return mejor_result, mejor_suma

#recibe el resultado y lo imprime en el formato pedido
def impresion_resultado(mejor_result):
    total = 0
    for i in range(len(mejor_result)):
        grupo, suma = mejor_result[i]
        grupo_str = ', '.join(grupo)
        print("Grupo " + str(i + 1) + ": " + grupo_str)
        total += (suma * suma)
    print("Coeficiente: " + str(total))


def main():
    archivo = input("Ingrese nombre del archivo:\n")
    grupos, maestros = carga(archivo)

    result_Greedy = sol_Greedy(maestros, len(grupos))
    suma_Greedy = sum(tot * tot for _, tot in result_Greedy)

    maestros.sort(key=lambda x: x[1], reverse=True)

    resultado_backtracking, _ = backtracking(maestros, 0, grupos, result_Greedy, suma_Greedy, len(grupos), set())

    impresion_resultado(resultado_backtracking)


main()