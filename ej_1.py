import csv
import sys


class Investigador:
    def __init__(self, nombre: str, peso: int, valor: int):
        self.nombre = nombre
        self.peso = peso
        self.valor = valor


def crearListaDeInvestigadores(filename):
    listaDeInvestigadores = [None]
    contadorInvestigadores = 1

    with open(filename, "r") as file:
        lector = csv.reader(file)
        for fila in lector:
            contadorInvestigadores += 1
            nombre = fila[0]
            peso = int(fila[1])
            valor = int(fila[2])
            listaDeInvestigadores.append(Investigador(nombre, peso, valor))

    return listaDeInvestigadores, contadorInvestigadores


investigadores = []
cantidadPersonas = 0
personasMaximas = 0
pesoMaximo = 0
OPT = []


def inicializarOPT(_cantidadPersonas, _pesoMaximo, _personasMaximas):
    global OPT

    OPT = []
    # O(n * p * w)
    for _ in range(_pesoMaximo + 1):
        OPT.append(
            [
                [(0, (0, 0, 0), 0) for _ in range(_cantidadPersonas)]
                for _ in range(_personasMaximas + 1)
            ]
        )


inicializarOPT(cantidadPersonas, pesoMaximo, personasMaximas)


def encontrarViajeOptimo():
    global investigadores
    global cantidadPersonas
    global personasMaximas
    global pesoMaximo
    global OPT
    # O(n * p * w)
    for k in range(1, pesoMaximo + 1):
        for j in range(1, personasMaximas + 1):
            for i in range(1, cantidadPersonas):
                if k < investigadores[i].peso:
                    OPT[k][j][i] = OPT[k][j][i - 1]
                else:
                    OPT[k][j][i] = max(
                        OPT[k][j][i - 1],
                        (
                            OPT[k - investigadores[i].peso][j - 1][i - 1][0]
                            + investigadores[i].valor,
                            (k - investigadores[i].peso, j - 1, i - 1),
                            i,
                        ),
                    )


def reconstruirSolucion():
    global investigadores
    global cantidadPersonas
    global personasMaximas
    global pesoMaximo
    global OPT

    investigadoresElegidos = []
    pesoOcupado = 0
    gananciaFinal = 0
    k, j, i = pesoMaximo, personasMaximas, cantidadPersonas - 1
    while i > 0:
        investigadoresElegidos.append(investigadores[OPT[k][j][i][2]])
        pesoOcupado += investigadores[OPT[k][j][i][2]].peso
        gananciaFinal += investigadores[OPT[k][j][i][2]].valor
        k, j, i = OPT[k][j][i][1]
    return gananciaFinal, pesoOcupado, investigadoresElegidos


def resetGlobals():
    global investigadores
    global cantidadPersonas
    global personasMaximas
    global pesoMaximo
    global OPT

    investigadores = []
    cantidadPersonas = 0
    personasMaximas = 0
    pesoMaximo = 0
    OPT = []


def main(filename, _personasMaximas, _pesoMaximo):
    resetGlobals()
    global pesoMaximo
    global personasMaximas

    if filename is None:
        filename = input("Ingrese la ubicación del archivo: ")
        personasMaximas = int(
            input("Ingrese la cantidad máxima de personas del transbordador: ")
        )
        pesoMaximo = int(
            input("Ingrese el peso máximo soportado por el transbordador: ")
        )
    else:
        personasMaximas = _personasMaximas
        pesoMaximo = _pesoMaximo

    global investigadores
    global cantidadPersonas

    investigadores, cantidadPersonas = crearListaDeInvestigadores(filename)
    inicializarOPT(cantidadPersonas, pesoMaximo, personasMaximas)
    encontrarViajeOptimo()

    gananciaFinal, pesoFinal, investigadoresElegidos = reconstruirSolucion()
    return gananciaFinal, pesoFinal, investigadoresElegidos


def imprimirResultados(gananciaFinal, pesoFinal, investigadoresElegidos):
    nombres = []
    ganancias = []
    pesos = []
    for investigador in investigadoresElegidos:
        nombres.append(f"{investigador.nombre}")
        pesos.append(f"{investigador.peso}")
        ganancias.append(f"{investigador.valor}")

    mensajeNombres = ", ".join(nombres)
    mensajePesos = " + ".join(pesos)
    mensajeGanancias = " + ".join(ganancias)

    print("Pasajeros: ", mensajeNombres)
    print("Peso total: ", mensajePesos, f"= {pesoFinal}")
    print("Ganancia: ", mensajeGanancias, f"= {gananciaFinal}")


if __name__ == "__main__":
    argc = len(sys.argv)

    if argc < 4:
        gananciaFinal, pesoFinal, investigadoresElegidos = main(None, None, None)
    else:
        filename = sys.argv[1]
        _cantidadMaximaPersonas = int(sys.argv[2])
        _pesoMaximo = int(sys.argv[3])
        print(filename, _cantidadMaximaPersonas, _pesoMaximo)
        gananciaFinal, pesoFinal, investigadoresElegidos = main(
            filename, _cantidadMaximaPersonas, _pesoMaximo
        )

    imprimirResultados(gananciaFinal, pesoFinal, investigadoresElegidos)
