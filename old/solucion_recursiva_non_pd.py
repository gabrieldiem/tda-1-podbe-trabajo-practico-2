class Investigador:
    def __init__(self, nombre, peso, valor):
        self.nombre = nombre
        self.peso = peso
        self.valor = valor

class Viaje:
    def __init__(self):
        self.viajeros = {}
        self.__valor__ = 0
        self.__peso__ = 0
    
    def agregar_investigador(self, investigador):
        self.viajeros[investigador.nombre] = investigador
        self.__valor__ += investigador.valor
        self.__peso__ += investigador.peso
        return self
    
    def remover_investigador(self, investigador):
        if investigador.nombre in self.viajeros:    
            del self.viajeros[investigador.nombre]
            self.__valor__ -= investigador.valor
            self.__peso__ -= investigador.peso
        return self

    def valor_total(self):
        return self.__valor__
    
    def peso_total(self):
        return self.__peso__

def opt(investigadores, i, peso, capacidad, viaje):
    if (i < 0) or (capacidad == 0):
        return Viaje()

    if (investigadores[i].peso > peso):
        return opt(investigadores, i - 1, peso, capacidad, viaje)
    
    a = opt(investigadores, i - 1, peso - investigadores[i].peso, capacidad - 1, viaje).agregar_investigador(investigadores[i])
    b = opt(investigadores, i - 1, peso, capacidad, viaje)

    return a if a.valor_total() > b.valor_total() else b

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
viaje = Viaje()

capacidad = 5
peso = 1000

ans = opt(investigadores, len(investigadores) - 1, peso, capacidad, viaje)

print("Valor total: ", ans.valor_total())
print("Peso total: ", ans.peso_total())
print("Viajeros: ", [i.nombre for i in ans.viajeros.values()])
