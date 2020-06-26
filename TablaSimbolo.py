class Simbolo:
    def __init__(self,*args):
        self.id = args[0]
        self.temporal = args[1]
        self.line = args[2]
        self.column = args[3]

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
        self.padre = None
    #Metodo para agregar un simbolo a la tabla de simbolos
    def add(self, simbolo):
        self.simbolos[simbolo.id] = simbolo   
    #Metodo que indica si existe variable en la tabla de simbolos
    def existe(self, id):
        return id in self.simbolos
    def setPadre(self, ts):
        self.padre = ts
    def getPadre(self):
        return self.padre
    def existePadre(self, id,ts):
        return self.__comprobar(id,ts)
    def __comprobar(self, id, ts):
        if id in ts.simbolos:
            return True
        if ts.padre:
            return self.__comprobar(id,ts.padre)
        return False

    def getValor(self, id, ts):
        if id in ts.simbolos:
            return ts.simbolos[id]
        if ts.padre:
            return self.getValor(id,ts.padre)
        return None

class Cuadruplo:
    def __init__(self, operador, arg1, arg2, result):
        self.op = operador
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

class Cuadruplos:
    def __init__(self):
        self.cuadruplos = []
        super().__init__()
        self.index_temporal = 0

    def add(self, cuadruplo):
        self.cuadruplos.append(cuadruplo)

class NodoStruct:
    def __init__(self,id):
        self.id = id

class TablaStruct:
    def __init__(self,id):
        self.atributos = []
        self.indice = 0
        self.id = id
    def add(self, valor):
        self.atributos.append(valor)

    def generarStruct(self):
        #generamos una nueva etiqueta
        salida = "{0}[{1}]".format(self.id,self.indice)
        #aumentamos su contador para que no existan mismos temporales
        self.indice += 1
        return salida