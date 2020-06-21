class Instruccion:
    'Clase para interfaz'

class Declaraciones(Instruccion):
    def __init__(self, tipo, declaraciones):
        self.tipo = tipo
        self.declaraciones = declaraciones
        super().__init__()

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
        self.parametros = params
        self.sentencias = sentencias

class Funcion(Instruccion):
    def __init__(self,tipo, id, params, sentencias):
        self.tipo = tipo
        self.id = id
        self.parametros = params
        self.sentencias = sentencias

class AsignacionSimple(Instruccion):
    def __init__(self, id, valor):
        self.id = id
        self.valor = valor

class AsignacionCompuesta(Instruccion):
    def __init__(self, id, op1, operacion):
        self.id = id
        self.operadorIzq = op1
        self.operacion = operacion

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

class OperacionNumero(Instruccion):
    def __init__(self,num, line, column):
        self.val = num
        self.line = line
        self.column = column

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