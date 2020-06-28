import sys
sys.path.append('./augus')
from enum import Enum
import subprocess
from ArbolCaracteres import *
from Arreglo import Arreglo
class Tipo(Enum):
    ENTERO = 1
    DECIMAL = 2
    STRING = 3
    CHAR = 4

class Tipo_Simbolo(Enum):
    TEMPORAL = 1
    MAIN = 2
    ETIQUETA = 3
    PARAMETRO = 4
    RETORNO = 5
    SIMULADOR = 6
    PILA = 7
    PUNTERO = 8
    INVALIDO = 9

class  Tipo_Etiqueta(Enum):
    FUNCION = 1
    PROCEDIMIENTO = 2
    CONTROL = 3
    MAIN = 4
    VARIABLE = 5
    ETIQUETA = 6
    ARREGLO = 7
    ARREGLONUMERICO =8
    STRUCT = 9

class Tipo_Salida(Enum):
    EXIT=1
    DESCARTAR = 2
    SEGUIR = 3

#clase para simular un apuntador
class ref:
    def __init__(self, valor):
        self.val = valor
    def set(self, new_val):
        self.val = new_val
    def get(self):
        return self.val

class Simbolo:
    def __init__(self, *args):
        self.id = args[0]
        self.sentencias = args[1]
        self.valor = ref(args[2])
        self.tipo = args[3]
        self.ambiente = args[4]
        self.etiqueta = args[5]
        self.line = args[6]
        self.column = args[7]


'''
Clase Tabla de Simbolo donde se almacenaran los  simbolos pertenecientes a recoleccion de datos de la primera pasada
    y posteriormente su ejecucion.
'''
class TablaSimbolosA:
    def __init__(self):
        self.simbolos = {}

    #Metodo para agregar un simbolo a la tabla de simbolos
    def add(self, simbolo):
        self.simbolos[simbolo.id] = simbolo
    #Metodo para obtener un simbolo teniendo su id
    def get(self, id):
        return self.simbolos[id]
    def set(self,id,valor):
        self.simbolos[id].valor.set(valor)
    #Metodo para actualizar un simbolo
    def actualizar(self,simbolo):
        self.simbolos[simbolo.id].valor.set(simbolo.valor.get())  
    def copy(self,id,simbolo):
        self.simbolos[id] = simbolo
    def delete(self,id):
        del self.simbolos[id]
    #Metodo que indica si existe variable en la tabla de simbolos
    def existe(self, id):
        return id in self.simbolos
    #Metodo para referenciar una variable
    def referenciar(self, id, valor):
        self.simbolos[id].valor = valor
    #Metodo para actualizar etiqueta
    def etiqueta(self, id, etiqueta):
        self.simbolos[id].etiqueta = etiqueta
    #Metodo para graficar simbolos
    def graficarSimbolos(self):
        try:
            file = open("tablasimbolos.dot", "w")
            file.write("digraph tabla{\n")
            file.write("graph [ratio=fill];node [label=\"\\N\", fontsize=15, shape=plaintext];\n")
            file.write("graph [bb=\"0,0,352,154\"];\n")
            file.write("arset [label=<")
            file.write("<TABLE ALIGN=\"LEFT\">\n")
            file.write("<TR><TD>IDENTIFICADOR</TD><TD>VALOR</TD><TD>TIPO</TD><TD>AMBIENTE</TD><TD>ETIQUETA</TD><TD>LINEA</TD><TD>COLUMNA</TD></TR>\n")
            for id in self.simbolos:
                file.write("<TR>")
                file.write("<TD>")
                file.write(self.simbolos[id].id)
                file.write("</TD>")
                file.write("<TD>")
               
                if isinstance(self.simbolos[id].valor.get(),ArbolCaracteres):
                    arbol = self.simbolos[id].valor.get()
                    file.write(arbol.getText())
                elif isinstance(self.simbolos[id].valor.get(),Arreglo):
                    file.write("ARREGLO")
                else:
                    file.write(str(self.simbolos[id].valor.get()))
                file.write("</TD>")
                file.write("<TD>")
                file.write(str(self.simbolos[id].tipo))
                file.write("</TD>")
                file.write("<TD>")
                file.write(self.simbolos[id].ambiente)
                file.write("</TD>")
                file.write("<TD>")
                file.write(str(self.simbolos[id].etiqueta))
                file.write("</TD>")
                file.write("<TD>")
                file.write(str(self.simbolos[id].line+1))
                file.write("</TD>")
                file.write("<TD>")
                file.write(str(self.simbolos[id].column))
                file.write("</TD>")
                file.write("</TR>\n")
            file.write("</TABLE>")
            file.write("\n>, ];\n")
            file.write("}")
        except:
            print("ERROR AL ESCRIBIR TABLA")
        finally:
            file.close()
            self.cmd("dot -Tpng tablasimbolos.dot -o tablasimbolos.png")

    def cmd(self,commando):
        subprocess.run(commando, shell=True)