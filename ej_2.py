import sys
import csv
import pulp


def leerArchivoActores(filename):
    actores = {}
    papeles = set()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            actor = row[0]
            actores[actor] = []
            for i in range(1, len(row), 2):
                papel = int(row[i])
                potencialidad = int(row[i + 1])
                actores[actor].append((papel, potencialidad))
                papeles.add(papel)

    return actores, papeles


# Función para obtener el valor que sigue a un número dado
def obtener_valor(dado, lista):
    return next((valor for clave, valor in lista if clave == dado), 0)


def resolverAsignacion(actores, papeles):
    # Definimos el problema de programación lineal(PL)
    problema = pulp.LpProblem("MaximizarPotencialesEspectadores", pulp.LpMaximize)

    # Definimos nuestras variables de decisión
    decisiones = pulp.LpVariable.dicts("x",
                                       (list(actores.keys()), list(papeles)),
                                       cat='Binary')

    # Definimos maximizar la potencialidad total
    problema += pulp.lpSum(obtener_valor(p, actores[a]) * decisiones[a][p] for a in actores for p in papeles), "Total_de_Espectadores"

    # Cada actor puede ser asignado a lo sumo a un papel(Restricción [1])
    for a in list(actores.keys()):
        problema += pulp.lpSum(decisiones[a][p] for p in papeles) <= 1, f"Actor_{a}_max_un_papel"

    # Cada papel puede ser asignado a lo sumo a un actor(Restricción[2])
    for p in papeles:
        problema += pulp.lpSum(decisiones[a][p] for a in actores) <= 1, f"Papel_{p}_max_un_actor"

    problema.solve()

    haySolucionOptima = pulp.LpStatus[problema.status] == "Optimal"
    return decisiones, haySolucionOptima


def imprimirResultados(haySolucionOptima, actores, decisiones):
    if not haySolucionOptima:
        print("══════════════════════════════════════════════════════════")
        print("No se encontró una solución óptima.")
        print("══════════════════════════════════════════════════════════")
        return

    print("══════════════════════════════════════════════════════════")
    print("Asignacion óptima de actores a papeles: ")
    potencialidad_total = 0
    for actor in actores:
        for papel, potencialidad in actores[actor]:
            if pulp.value(decisiones[actor][papel]) == 1:
                print(
                    f"Actor: [{actor}] asignado al papel [{papel}] con potencialidad: [{potencialidad}]"
                )
                potencialidad_total += potencialidad

    print(f"Potencialidad total de espectadores: [{potencialidad_total}]")
    print("══════════════════════════════════════════════════════════")


def main(filename):
    if filename is None:
        filename = input("Ingrese la ubicación del archivo: ")

    actores, papeles = leerArchivoActores(filename)
    decisiones, haySolucionOptima = resolverAsignacion(actores, papeles)
    imprimirResultados(haySolucionOptima, actores, decisiones)


if __name__ == "__main__":
    argc = len(sys.argv)

    if argc < 2:
        a = main(None)
    else:
        filename = sys.argv[1]
        a = main(filename)
