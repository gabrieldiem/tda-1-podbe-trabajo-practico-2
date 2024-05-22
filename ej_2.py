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


def resolverAsignacion(actores, papeles):
    # Definimos el problema de programación lineal(PL)
    problema = pulp.LpProblem("AsignarActores", pulp.LpMaximize)

    # Definimos nuestras variables de decisión
    decisiones = pulp.LpVariable.dicts(
        "x",
        ((actor, papel) for actor in actores for papel, _ in actores[actor]),
        cat="Binary",
    )

    # Definimos maximizar la potencialidad total
    problema += pulp.lpSum(
        [
            potencialidad * decisiones[(actor, papel)]
            for actor in actores
            for papel, potencialidad in actores[actor]
        ]
    )

    # Cada actor puede ser asignado a lo sumo a un papel(Restricción [1])
    for actor in actores:
        problema += (
            pulp.lpSum([decisiones[(actor, papel)] for papel, _ in actores[actor]])
            <= 1,
            f"UnPapelPorActor_{actor}",
        )

    # Cada papel puede ser asignado a lo sumo a un actor(Restricción[2])
    for papel in papeles:
        problema += (
            pulp.lpSum(
                [decisiones(actor, papel)]
                for actor in actores
                if (papel, actor) in actores[actor]
            )
            <= 1,
            f"UnActorPorPapel_{papel}",
        )

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
            if pulp.value(decisiones[(actor, papel)]) == 1:
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
