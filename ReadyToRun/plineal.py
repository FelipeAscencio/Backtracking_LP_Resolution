import pulp

PRIMER_RENGLON = 2

#recibe el nombre del archivo y devuelve una lista de tuplas de (maestro, poder) y una lista de listas vacias (grupos)
def carga(archivo):
    try:
        nombre_archivo = archivo + ".txt"
        with open(nombre_archivo) as archivo:
            lineas = archivo.readlines()
            num_grupos = int(lineas[1].strip())
            grupos = [([], 0) for _ in range(num_grupos)]
            maestros = {}
            for linea in lineas[PRIMER_RENGLON:]:  # O(n)
                datos = linea.strip().split(",")
                maestros[datos[0]] = int(datos[1])
        return grupos, maestros
    except IOError:
        print("Error al abrir el archivo")
        return None

#Resuelve el problema por programacion lineal entera, busca minimizar la resta entre el grupo mas poderoso y el menos poderoso
def Grupos_balanceados(maestros, k):
    nombres = list(maestros.keys())
    poderes = list(maestros.values())

    prob = pulp.LpProblem("Grupos_balanceados", pulp.LpMinimize)

    y = pulp.LpVariable.dicts("y", ((i, j) for i in range(len(nombres)) for j in range(k)), cat='Binary')
    z = pulp.LpVariable.dicts("z", range(k), cat='Continuous')
    Z_max = pulp.LpVariable("Z_max", cat='Continuous')
    Z_min = pulp.LpVariable("Z_min", cat='Continuous')


    for i in range(len(nombres)):
        prob += pulp.lpSum(y[i, j] for j in range(k)) == 1

    for j in range(k):
        prob += z[j] == pulp.lpSum(poderes[i] * y[i, j] for i in range(len(nombres)))

    for j in range(k):
        prob += Z_max >= z[j]
        prob += Z_min <= z[j]

    prob += Z_max - Z_min
    prob.solve()

    resultado = [([], 0)] * k
    for i in range(len(nombres)):
        for j in range(k):
            if pulp.value(y[i, j]) == 1:
                guerreros, sumatoria = resultado[j]
                resultado[j] = (guerreros + [nombres[i]], sumatoria + poderes[i])
    return resultado

#recibe el resultado y lo imprime en el formato pedido
def impresion_resultado(mejor_result):
    total = 0
    for i in  range(len(mejor_result)):
        grupo, suma = mejor_result[i]
        grupo_str = ', '.join(grupo)
        print("Grupo " + str(i+1) + ": " + grupo_str)
        total += (suma*suma)
    print("Coeficiente: " + str(total))


def main():
    archivo = input("Ingrese nombre del archivoPL\n")
    grupos, maestros = carga(archivo)
    resultado_PL = Grupos_balanceados(maestros, len(grupos))
    impresion_resultado(resultado_PL)


main()