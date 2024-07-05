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
def sol_Greedy2(maestros, num_grupos):
    maestros_ordenados2 = sorted(maestros, key=lambda x: x[1], reverse=True)
    resultado2 = [([], 0)] * num_grupos
    ida = True
    grupo = 0
    for guerrero in maestros_ordenados2:
        guerreros, sumatoria = resultado2[grupo]
        resultado2[grupo] = (guerreros + [guerrero[0]], sumatoria + guerrero[1])
        if ida:
            grupo += 1
            if grupo == num_grupos:
                grupo = num_grupos - 1
                ida = False
        else:
            grupo -= 1
            if grupo == -1:
                grupo = 0
                ida = True
    return resultado2

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

    result_Greedy2 = sol_Greedy2(maestros, len(grupos))

    impresion_resultado(result_Greedy2)


main()