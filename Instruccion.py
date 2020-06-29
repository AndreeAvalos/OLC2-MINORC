class Instruccion:
    'Clase para interfaz'

class Declaraciones(Instruccion):
    def __init__(self, tipo, declaraciones, line):
        self.tipo = tipo
        self.declaraciones = declaraciones
        self.line =line
        super().__init__()

class DeclaracionesStruct(Instruccion):
    def __init__(self, tipo, declaraciones, line):
        self.tipo = tipo
        self.declaraciones = declaraciones
        self.line =line
        super().__init__()

class DeclaracionesArreglo(Instruccion):
    def __init__(self, tipo, declaraciones, line):
        self.tipo = tipo
        self.declaraciones = declaraciones
        self.line =line

class Arreglo(Instruccion):
    def __init__(self, id, dimensiones, valores, line):
        self.id = id 
        self.dimensiones = dimensiones
        self.valores = valores
        self.line =line

class DeclaracionesArregloStruct(Instruccion):
    def __init__(self, tipo, declaraciones, line):
        self.tipo = tipo
        self.declaraciones = declaraciones
        self.line =line

class ArregloStruct(Instruccion):
    def __init__(self, id, dimensiones, line):
        self.id = id 
        self.dimensiones = dimensiones
        self.line =line

class Declaracion(Instruccion):
    def __init__(self, id, valor, line, column):
        self.id = id
        self.line = line
        self.column = column
        #Si valor es none es porque no tiene asignacion.
        self.valor = valor
class Main(Instruccion):
    def __init__(self, sentencias, line):
        self.sentencias = sentencias
        self.line = line

class Metodo(Instruccion):
    def __init__(self, id, params, sentencias, line):
        self.id = id
        self.params = params
        self.sentencias = sentencias
        self.line =line

class Funcion(Instruccion):
    def __init__(self,tipo, id, params, sentencias, line):
        self.tipo = tipo
        self.id = id
        self.params = params
        self.sentencias = sentencias
        self.line =line

class Llamada(Instruccion):
    def __init__(self,id,params, line):
        self.id = id
        self.params = params
        self.line =line


class AsignacionSimple(Instruccion):
    def __init__(self, id, valor, line):
        self.id = id
        self.valor = valor
        self.line =line

class AsignacionCompuesta(Instruccion):
    def __init__(self, id, op1, operacion, line):
        self.id = id
        self.operadorIzq = op1
        self.operacion = operacion
        self.line =line

class AsignacionStruct(Instruccion):
    def __init__(self, id, atributos, operacion, line):
        self.id = id
        self.atributos = atributos
        self.operacion = operacion
        self.line =line

class Atributo(Instruccion):
    def __init__(self, id, indices, line):
        self.id = id
        self.indices = indices
        self.line =line

class AsignacionArreglo(Instruccion):
    def __init__(self, id, indices, operacion, line):
        self.id = id
        self.indices = indices
        self.operacion = operacion
        self.line =line

class AsignacionArregloStruct(Instruccion):
    def __init__(self, id, indices,atributos, operacion, line):
        self.id = id
        self.indices = indices
        self.atributos = atributos
        self.operacion = operacion
        self.line =line


class If(Instruccion):
    def __init__(self,s_if, s_elif, s_else ):
        self.s_if = s_if #sentencia if
        self.s_elif = s_elif #lista de sentencias if
        self.s_else = s_else #sentencia else
    
class SentenciaIf(Instruccion):
    def __init__(self, condicion, sentencias, line):
        self.condicion = condicion
        self.sentencias = sentencias
        self.line =line
        
class While(Instruccion):
    def __init__(self, condicion, sentencias, line):
        self.condicion = condicion
        self.sentencias = sentencias
        self.line =line

class DoWhile(Instruccion):
    def __init__(self, condicion, sentencias, line):
        self.condicion = condicion
        self.sentencias = sentencias
        self.line =line

class For(Instruccion):
    def __init__(self, inicializacion, condicion, incremento, sentencias, line):
        self.inicializacion = inicializacion
        self.condicion = condicion
        self.incremento = incremento
        self.sentencias = sentencias
        self.line =line

class Switch(Instruccion):
    def __init__(self, condicion,casos, line):
        self.condicion = condicion
        self.casos = casos
        self.line =line

class Case(Instruccion):
    def __init__(self, operacion, sentencias, line):
        self.operacion = operacion
        self.sentencias = sentencias
        self.line =line

class Continue(Instruccion):
    def __init__(self, line):
        self.line =line
        super().__init__()
        
class Break(Instruccion):
    def __init__(self, line):
        self.line =line
        super().__init__()

class Struct(Instruccion):
    def __init__(self, id, declaraciones, line):
        self.id = id
        self.declaraciones = declaraciones
        self.line =line

class Return(Instruccion):
    def __init__(self, operacion, line):
        self.operacion = operacion
        self.line =line

class Scan(Instruccion):
    def __init__(self):
        super().__init__()

class Print(Instruccion):
    def __init__(self, cadena, argumentos, line):
        self.cadena = cadena
        self.argumentos = argumentos
        self.line =line

class GoTo(Instruccion):
    def __init__(self,id, line):
        self.id = id
        self.line =line

class Etiqueta(Instruccion):
    def __init__(self,id, line):
        self.id = id
        self.line =line       

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