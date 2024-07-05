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

    impresion_resultado(result_Greedy)


main()