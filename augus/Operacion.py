import sys
sys.path.append('./augus')
from enum import Enum
from InstruccionA import Instruccion

class OPERACION_LOGICA(Enum):
    AND = 1
    OR = 2
    NOT = 3
    XOR = 4 


class OPERACION_RELACIONAL(Enum):
    MAYOR = 1
    MAYORQUE = 2
    MENOR = 3
    MENORQUE = 4
    IGUAL = 5
    DIFERENTE = 6

class OPERACION_NUMERICA(Enum):
    SUMA = 1
    RESTA = 2
    MULTIPLICACION = 3
    DIVISION = 4
    MODULAR = 5
    ABSOLUTO = 6

class OPERACION_BIT(Enum):
    NOT = 1
    AND = 2
    OR = 3
    XOR = 4
    SHIFTIZQ = 5
    SHIFTDER = 6
    APUNTAR = 7

class OperacionNumerica(Instruccion):
    def __init__(self, op1, op2, operacion, line, column):
        self.operadorIzq = op1
        self.operadorDer = op2
        self.operacion = operacion
        self.line =line
        self.column = column

class OperacionLogica(Instruccion):
    def __init__(self, op1, op2, operacion, line, column):
        self.operadorIzq = op1
        self.operadorDer = op2
        self.operacion = operacion
        self.line =line
        self.column = column

class OperacionRelacional(Instruccion):
    def __init__(self, op1, op2, operacion, line, column):
        self.operadorIzq = op1
        self.operadorDer = op2
        self.operacion = operacion
        self.line =line
        self.column = column

class OperacionBit(Instruccion):
    def __init__(self, op1, op2, operacion, line, column):
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
class OperacionCopiaVariable(Instruccion):
    def __init__(self,id, line, column):
        self.id = id
        self.line =line
        self.column = column

class OperacionCadena(Instruccion):
    def __init__(self,num, line, column):
        self.val = num
        self.line = line
        self.column = column
        
class OperacionArreglo(Instruccion):
    def __init__(self,id, dimensiones,line, column):
        self.id = id
        self.dimensiones = dimensiones
        self.line =line
        self.column = column

class OperacionCasteo(Instruccion):
    def __init__(self,tipo,id,line, column):
        self.tipo = tipo
        self.expresion = id
        self.line = line
        self.column = column