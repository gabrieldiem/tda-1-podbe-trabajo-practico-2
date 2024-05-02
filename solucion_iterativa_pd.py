class Investigador:
    def __init__(self, nombre, peso, valor):
        self.nombre = nombre
        self.peso = peso
        self.valor = valor

input = [
("Alan Turing",300,1000),
("John von Neumann",50,500),
("Grace Murray Hopper",400,300),
("Dennis Ritchie",200,450),
("Claude Shannon",50,100),
("Marvin Minsky",500,650),
("Tim Berners-Lee",250,500)
]

investigadores = [Investigador(i[0], i[1], i[2]) for i in input]
cantidadPersonas = len(investigadores)
selecteds = []
for i in range(cantidadPersonas):
    selecteds.append(0)


personasMaximas = 4
pesoMaximo = 500
OPT = list(list(list()))

OPT = []
for i in range(cantidadPersonas):
    row = []
    for j in range(pesoMaximo):
        col = []
        for k in range(personasMaximas):
            col.append(0)
        row.append(col)
    OPT.append(row)

#print(OPT)

pesoDisponible = pesoMaximo
espaciosDisponibles = personasMaximas

def hayCapacidadDisponible(_personaActual, _pesoDisponible, _espaciosDisponibles):
    if _espaciosDisponibles == 0:
        return False
    return _pesoDisponible >= investigadores[_personaActual].peso

def incluirPersonaActual(_personaActual, _pesoDisponible, _nuevoPeso, _espaciosDisponibles):
    gananciaAnterior = 0
    if personaActual > 1:
        gananciaAnterior = OPT[_personaActual-1][_pesoDisponible][_espaciosDisponibles]
    OPT[_personaActual][_nuevoPeso][_espaciosDisponibles-1] = gananciaAnterior + investigadores[_personaActual].valor
    selecteds[_personaActual] = 1

for personaActual in range(0, cantidadPersonas-1):
    if hayCapacidadDisponible(personaActual, pesoDisponible, espaciosDisponibles) == False:
        if personaActual > 1:
            OPT[personaActual][pesoDisponible][espaciosDisponibles] = OPT[personaActual-1][pesoDisponible][espaciosDisponibles]
        continue
    
    gananciaSinPersonaActual = 0
    if personaActual > 1:
        gananciaSinPersonaActual = OPT[personaActual-1][pesoDisponible][espaciosDisponibles]
    nuevoPeso = pesoDisponible - investigadores[personaActual].peso
    incluirPersonaActual(personaActual, pesoDisponible, nuevoPeso, espaciosDisponibles)
    gananciaConPersonaActual = OPT[personaActual][nuevoPeso][espaciosDisponibles-1]
    
    if gananciaSinPersonaActual > gananciaConPersonaActual:
        OPT[personaActual][nuevoPeso][espaciosDisponibles-1] = gananciaSinPersonaActual
        OPT[personaActual][pesoDisponible][espaciosDisponibles] = gananciaSinPersonaActual
        selecteds[personaActual] = 0
    else:
        espaciosDisponibles = espaciosDisponibles -1
        pesoDisponible = nuevoPeso

for i in range(cantidadPersonas):
    if selecteds[i] == 1:
        print(investigadores[i].nombre)
