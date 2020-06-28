import sys
sys.path.append('./augus')

from InstruccionA import *
from Operacion import *
from TablaSimbolosA import Simbolo, TablaSimbolosA

class TokenError:
    def __init__(self,tipo, descripcion, line, column):
        self.tipo = tipo
        self.descripcion = descripcion
        self.line = line 
        self.column = column

class Recolectar:
    def __init__(self, instrucciones, ts, lst):
        self.intrucciones = instrucciones
        self.ts = ts
        self.lst_errores = lst

    def getErrores(self):
        return self.lst_errores

    def agregarError(self,descripcion,line,column):
        new_error = TokenError("Semantico",descripcion,line,column)
        self.lst_errores.append(new_error)

    def procesar(self):
        for instruccion in self.intrucciones:
            if isinstance(instruccion,Main): self.procesar_main(instruccion)
            elif isinstance(instruccion, Etiqueta): self.procesar_etiqueta(instruccion)

    def procesar_main(self,instruccion):
        new_simbol = Simbolo(instruccion.id, instruccion.sentencias, instruccion.valor, instruccion.tipo,"global",instruccion.etiqueta,instruccion.line,instruccion.column)
        if not self.ts.existe(instruccion.id):
            self.ts.add(new_simbol)
        else:
            self.agregarError("Ya se ha declarado la etiqueta main",instruccion.line,instruccion.column)
        
    
    def procesar_etiqueta(self,instruccion):
        new_simbol = Simbolo(instruccion.id, instruccion.sentencias, instruccion.valor, instruccion.tipo,"global",instruccion.etiqueta,instruccion.line,instruccion.column)
        if not self.ts.existe(instruccion.id):
            self.ts.add(new_simbol)
        else:
            self.agregarError("Ya se ha declarado la etiqueta "+instruccion.id,instruccion.line,instruccion.column)





