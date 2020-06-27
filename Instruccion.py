class Instruccion:
    'Clase para interfaz'

class Declaraciones(Instruccion):
    def __init__(self, tipo, declaraciones):
        self.tipo = tipo
        self.declaraciones = declaraciones
        super().__init__()

class DeclaracionesStruct(Instruccion):
    def __init__(self, tipo, declaraciones):
        self.tipo = tipo
        self.declaraciones = declaraciones
        super().__init__()

class DeclaracionesArreglo(Instruccion):
    def __init__(self, tipo, declaraciones):
        self.tipo = tipo
        self.declaraciones = declaraciones

class Arreglo(Instruccion):
    def __init__(self, id, dimensiones, valores):
        self.id = id 
        self.dimensiones = dimensiones
        self.valores = valores

class DeclaracionesArregloStruct(Instruccion):
    def __init__(self, tipo, declaraciones):
        self.tipo = tipo
        self.declaraciones = declaraciones

class ArregloStruct(Instruccion):
    def __init__(self, id, dimensiones):
        self.id = id 
        self.dimensiones = dimensiones

class Declaracion(Instruccion):
    def __init__(self, id, valor, line, column):
        self.id = id
        self.line = line
        self.column = column
        #Si valor es none es porque no tiene asignacion.
        self.valor = valor
class Main(Instruccion):
    def __init__(self, sentencias):
        self.sentencias = sentencias

class Metodo(Instruccion):
    def __init__(self, id, params, sentencias):
        self.id = id
        self.params = params
        self.sentencias = sentencias

class Funcion(Instruccion):
    def __init__(self,tipo, id, params, sentencias):
        self.tipo = tipo
        self.id = id
        self.params = params
        self.sentencias = sentencias

class Llamada(Instruccion):
    def __init__(self,id,params):
        self.id = id
        self.params = params


class AsignacionSimple(Instruccion):
    def __init__(self, id, valor):
        self.id = id
        self.valor = valor

class AsignacionCompuesta(Instruccion):
    def __init__(self, id, op1, operacion):
        self.id = id
        self.operadorIzq = op1
        self.operacion = operacion

class AsignacionStruct(Instruccion):
    def __init__(self, id, atributos, operacion):
        self.id = id
        self.atributos = atributos
        self.operacion = operacion

class Atributo(Instruccion):
    def __init__(self, id, indices):
        self.id = id
        self.indices = indices

class AsignacionArreglo(Instruccion):
    def __init__(self, id, indices, operacion):
        self.id = id
        self.indices = indices
        self.operacion = operacion

class AsignacionArregloStruct(Instruccion):
    def __init__(self, id, indices,atributos, operacion):
        self.id = id
        self.indices = indices
        self.atributos = atributos
        self.operacion = operacion


class If(Instruccion):
    def __init__(self,s_if, s_elif, s_else ):
        self.s_if = s_if #sentencia if
        self.s_elif = s_elif #lista de sentencias if
        self.s_else = s_else #sentencia else
    
class SentenciaIf(Instruccion):
    def __init__(self, condicion, sentencias):
        self.condicion = condicion
        self.sentencias = sentencias
        
class While(Instruccion):
    def __init__(self, condicion, sentencias):
        self.condicion = condicion
        self.sentencias = sentencias

class DoWhile(Instruccion):
    def __init__(self, condicion, sentencias):
        self.condicion = condicion
        self.sentencias = sentencias

class For(Instruccion):
    def __init__(self, inicializacion, condicion, incremento, sentencias):
        self.inicializacion = inicializacion
        self.condicion = condicion
        self.incremento = incremento
        self.sentencias = sentencias

class Switch(Instruccion):
    def __init__(self, condicion,casos):
        self.condicion = condicion
        self.casos = casos

class Case(Instruccion):
    def __init__(self, operacion, sentencias):
        self.operacion = operacion
        self.sentencias = sentencias
        
class Break(Instruccion):
    def __init__(self):
        super().__init__()

class Struct(Instruccion):
    def __init__(self, id, declaraciones):
        self.id = id
        self.declaraciones = declaraciones

class Return(Instruccion):
    def __init__(self, operacion):
        self.operacion = operacion

class Scan(Instruccion):
    def __init__(self):
        super().__init__()

class Print(Instruccion):
    def __init__(self, cadena, argumentos):
        self.cadena = cadena
        self.argumentos = argumentos

class OperacionAsignacion(Instruccion):
    def __init__(self, operacion, op1):
        self.operadorIzq = op1
        self.operacion = operacion


class OperacionBinaria(Instruccion):
    def __init__(self, op1, op2, operacion,line, column):
        self.operadorIzq = op1
        self.operadorDer = op2
        self.operacion = operacion
        self.line =line
        self.column = column

class OperacionUnaria(Instruccion):
    def __init__(self, op1, operacion, line, column):
        self.operadorIzq = op1
        self.operacion = operacion
        self.line =line
        self.column = column

class OperacionLlamada(Instruccion):
    def __init__(self,id,params):
        self.id = id
        self.params = params

class OperacionStruct(Instruccion):
    def __init__(self,id, atributos):
        self.id = id
        self.atributos = atributos

class OperacionArregloStruct(Instruccion):
    def __init__(self,id,indices,atributos):
        self.id = id
        self.indices = indices
        self.atributos = atributos

class OperacionNumero(Instruccion):
    def __init__(self,num, line, column):
        self.val = num
        self.line = line
        self.column = column
class OperacionArreglo(Instruccion):
    def __init__(self, id, indices):
        self.id = id
        self.indices = indices


class OperacionVariable(Instruccion):
    def __init__(self,id, line, column):
        self.id = id
        self.line =line
        self.column = column

class OperacionCadena(Instruccion):
    def __init__(self,num, line, column):
        self.val = num
        self.line = line
        self.column = column

class OperacionCaracter(Instruccion):
    def __init__(self,num, line, column):
        self.val = num
        self.line = line
        self.column = column

class OperacionTernaria(Instruccion):
    def __init__(self, condicion, op1, op2, line, column):
        self.condicion =condicion
        self.op1 = op1
        self.op2 = op2
        self.line = line
        self.column = column