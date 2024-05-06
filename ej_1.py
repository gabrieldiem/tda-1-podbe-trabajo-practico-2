import csv
import sys


class Investigador:
    def __init__(self, nombre: str, peso: int, valor: int):
        self.nombre = nombre
        self.peso = peso
        self.valor = valor


def crearListaDeInvestigadores(filename):
    listaDeInvestigadores = []
    contadorInvestigadores = 0
    
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
selecteds = []
personasMaximas = 0
pesoMaximo = 0
pesoDisponible = 0
espaciosDisponibles = 0
OPT = []

def inicializarOPT(_cantidadPersonas, _pesoMaximo, _personasMaximas):
    global OPT
    
    OPT = []
    for i in range(_cantidadPersonas):
        row = []
        for j in range(_pesoMaximo):
            col = []
            for k in range(_personasMaximas):
                col.append(0)
            row.append(col)
        OPT.append(row)

inicializarOPT(cantidadPersonas, pesoMaximo, personasMaximas)

def hayCapacidadDisponible(_personaActual, _pesoDisponible, _espaciosDisponibles):
    global investigadores
    
    print(_pesoDisponible, investigadores[_personaActual].peso)
    
    if _espaciosDisponibles == 0:
        return False
    return _pesoDisponible >= investigadores[_personaActual].peso


def incluirPersonaActual(_personaActual, _pesoDisponible, _nuevoPeso, _espaciosDisponibles):
    global investigadores
    global selecteds
    global OPT
    
    gananciaAnterior = 0
    if _personaActual > 0:
        gananciaAnterior = OPT[_personaActual - 1][_pesoDisponible][_espaciosDisponibles]
    OPT[_personaActual][_nuevoPeso][_espaciosDisponibles - 1] = gananciaAnterior + investigadores[_personaActual].valor
    selecteds[_personaActual] = 1


def encontrarViajeOptimo():
    global investigadores
    global cantidadPersonas
    global selecteds
    global personasMaximas
    global pesoMaximo
    global OPT
    global pesoDisponible
    global espaciosDisponibles
    #print(OPT)
    
    for personaActual in range(0, cantidadPersonas - 1):
        if hayCapacidadDisponible(personaActual, pesoDisponible, espaciosDisponibles) == False:
            if personaActual > 0:
                OPT[personaActual][pesoDisponible][espaciosDisponibles] = OPT[personaActual - 1][pesoDisponible][espaciosDisponibles]
            continue

        gananciaSinPersonaActual = 0
        if personaActual > 0:
            gananciaSinPersonaActual = OPT[personaActual - 1][pesoDisponible][espaciosDisponibles]
        nuevoPeso = pesoDisponible - investigadores[personaActual].peso
        incluirPersonaActual(personaActual, pesoDisponible, nuevoPeso, espaciosDisponibles)
        gananciaConPersonaActual = OPT[personaActual][nuevoPeso][espaciosDisponibles - 1]

        if gananciaSinPersonaActual > gananciaConPersonaActual:
            OPT[personaActual][nuevoPeso][espaciosDisponibles - 1] = gananciaSinPersonaActual
            OPT[personaActual][pesoDisponible][espaciosDisponibles] = gananciaSinPersonaActual
            selecteds[personaActual] = 0
        else:
            espaciosDisponibles = espaciosDisponibles - 1
            pesoDisponible = nuevoPeso

    gananciaFinal = 0
    pesoOcupado = 0
    investigadoresElegidos = []
    
    for i in range(cantidadPersonas):
        if selecteds[i] == 1:
            gananciaFinal += investigadores[i].valor
            pesoOcupado += investigadores[i].peso
            investigadoresElegidos.append(investigadores[i])
    
    return gananciaFinal, pesoOcupado, investigadoresElegidos


def resetGlobals():
    global investigadores
    global cantidadPersonas
    global selecteds
    global personasMaximas
    global pesoMaximo
    global OPT
    global pesoDisponible
    global espaciosDisponibles

    investigadores = []
    cantidadPersonas = 0
    selecteds = []
    personasMaximas = 0
    pesoMaximo = 0
    OPT = []
    pesoDisponible = 0
    espaciosDisponibles = 0


def inicializarSelecteds(cantidadPersonas):
    selecteds = []
    for i in range(cantidadPersonas):
        selecteds.append(0)
    return selecteds


def main(filename, _personasMaximas, _pesoMaximo):
    resetGlobals()
    global pesoMaximo
    global personasMaximas
    
    if filename is None:
        filename = input("Ingrese la ubicación del archivo: ")
        personasMaximas = int(input("Ingrese la cantidad máxima de personas del transbordador: "))
        pesoMaximo = int(input("Ingrese el peso máximo soportado por el transbordador: "))
    else:
        personasMaximas = _personasMaximas
        pesoMaximo = _pesoMaximo

    global investigadores
    global cantidadPersonas
    global selecteds
    global pesoDisponible
    global espaciosDisponibles

    investigadores, cantidadPersonas = crearListaDeInvestigadores(filename)
    selecteds = inicializarSelecteds(cantidadPersonas)
    pesoDisponible = pesoMaximo
    espaciosDisponibles = personasMaximas
    inicializarOPT(cantidadPersonas, pesoMaximo, personasMaximas)

    gananciaFinal, pesoFinal, investigadoresElegidos = encontrarViajeOptimo()
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
        gananciaFinal, pesoFinal, investigadoresElegidos = main(filename, _cantidadMaximaPersonas, _pesoMaximo)

    imprimirResultados(gananciaFinal, pesoFinal, investigadoresElegidos)
