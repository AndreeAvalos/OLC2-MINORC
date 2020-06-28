import sys
sys.path.append('./augus')

import ply.yacc as yacc
import ply.lex as lex

from InstruccionA import *
from Operacion import *
import subprocess
from Recolectar import TokenError


index =0 
lst_errores = []



def cmd(commando):
    subprocess.run(commando, shell=True)

class NodoGramatical:
    def __init__(self, produccion):
        self.produccion = produccion
        self.reglas = []
    def add(self,regla):
        self.reglas.append(regla)

class Nodo:
    def __init__(self,nodoast,nodog):
        self.instruccion = nodoast
        self.nodo = nodog

class NodoG:
    def __init__(self,indic, nombre, childs = []):
        self.index = indic
        self.nombre = nombre
        self.childs= childs
    def add(self, child):
        self.childs.append(child)


def agregarError(tipo,descripcion,line,column):
    global lst_errores
    new_error = TokenError(tipo,descripcion,line,column)
    lst_errores.append(new_error)

def graficarErrores():
    global lst_errores

    try:
        file = open("ELS.dot", "w")
        file.write("digraph tablaErrores{\n")
        file.write("graph [ratio=fill];node [label=\"\\N\", fontsize=15, shape=plaintext];\n")
        file.write("graph [bb=\"0,0,352,154\"];\n")
        file.write("arset [label=<")
        file.write("<TABLE ALIGN=\"LEFT\">\n")
        file.write("<TR><TD>TIPO</TD><TD>DESCRIPCION</TD><TD>LINEA</TD><TD>COLUMNA</TD></TR>\n")
        for token in lst_errores:
            file.write("<TR>")
            file.write("<TD>")
            file.write(token.tipo)
            file.write("</TD>")
            file.write("<TD>")
            file.write(token.descripcion)
            file.write("</TD>")
            file.write("<TD>")
            file.write(str(token.line))
            file.write("</TD>")
            file.write("<TD>")
            file.write(str(token.column))
            file.write("</TD>")
            file.write("</TR>\n")
        file.write("</TABLE>")
        file.write("\n>, ];\n")
        file.write("}")
    except:
        print("ERROR AL ESCRIBIR TABLA")
    finally:
        file.close()
        cmd("dot -Tpng ELS.dot -o ELS.png")

lstGrmaticales = [] #lista donde se almacenaran todas las producciones y sus reglas semanticas

reservadas = {
    #Tipos para castear
    'int': 'INTEGER',
    'float': 'FLOAT',
    'char': 'CHAR',
    'print': 'PRINT',
    'main': 'MAIN',
    'goto': 'GOTO',
    'unset': 'UNSET',
    'read': 'READ',
    'exit': 'EXIT',
    'if': 'IF',
    'abs': 'ABS',
    'xor': 'XOR',
    'array': 'ARRAY'
}

tokens = [
    'PYCOMA',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'IGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CADENA2',
    'ID',
    'MAS',
    'MENOS',
    'MULTIPLICACION',
    'DIVISION',
    'MODULAR',
    'NOT',
    'AND',
    'OR',
    'NOTBIT',
    'ANDBIT',
    'ORBIT',
    'XORBIT',
    'SHIFTIZQ',
    'SHIFTDER',
    'DOSPUNTOS',
    'VARIABLE'
] + list(reservadas.values())

t_PYCOMA = r';'
t_DOSPUNTOS = r':'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_IGUAL = r'='
t_IGUALIGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULAR = '%'
t_NOT = r'!'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOTBIT = r'~'
t_ANDBIT = r'&'
t_ORBIT = r'\|'
t_XORBIT = r'\^'
t_SHIFTIZQ = r'<<'
t_SHIFTDER = r'>>'
#t_ESCAPE =r'\"\\n\"'

t_ignore = " \t"

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error: %d ", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        #editar
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_VARIABLE(t):
     r'\$[a-z][a-z]*[0-9]*'
     t.type = reservadas.get(t.value.lower(),'VARIABLE')
     return t


def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CADENA2(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_COMENTARIO(t):
    r'\#.*'
    t.lexer.lineno += 1



def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    #editar para agregar a una tabla
    #print("Illegal character '%s'" % t.value[0])
    agregarError('Lexico',"Caracter \'{0}\' ilegal".format(t.value[0]), t.lexer.lineno+1,find_column(t))
    t.lexer.skip(1)


def getIndex():
    global index
    index = index+1
    return index

def p_init(p):
    'init : instrucciones'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("initi-> instrucciones")
    gramatical.add("init=instrucciones")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo2 = NodoG(getIndex(),"init", [])
    for item in p[1].nodo:
        nodo2.add(item)
    p[0] = Nodo(p[1].instruccion, nodo2)

def p_instrucciones(p):
    ''' instrucciones : instrucciones instruccion '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("instrucciones-> intrucciones2 instruccion")
    gramatical.add("instrucciones2.val.append(instruccion)")
    gramatical.add("instrucciones.val = instrucciones2.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[1].instruccion.append(p[2].instruccion)
    nodo2 = NodoG(getIndex(),"instruccion",[])
    nodo2.add(p[2].nodo)
    p[1].nodo.append(nodo2)
    nodo = NodoG(getIndex(),"instrucciones",p[1].nodo)
    p[0] = Nodo(p[1].instruccion,[nodo])
   

        
def p_instrucciones2(p):
    ' instrucciones : instruccion '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("instrucciones-> instruccion")
    gramatical.add("instru = []")
    gramatical.add("instru.append(instruccion)")
    gramatical.add("instrucciones.val = instru")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[0]= Nodo([p[1].instruccion],[NodoG(getIndex(),"instruccion",[p[1].nodo])])
    


def p_instruccion(p):
    ''' instruccion : pmain
                    | petiqueta'''
    p[0] = p[1]
    
def p_pmain(p):
    'pmain : MAIN DOSPUNTOS sentencias '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pmain-> MAIN DOSPUNTOS sentencias")
    gramatical.add("pmain.val = Main(sentencias.val)")
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("instruccion-> pmain")
    gramatical.add("instrucion = pmain")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo2 = NodoG(getIndex(),"pmain",[])
    nodo2.add(NodoG(getIndex(),"main", None))
    nodo2.add(NodoG(getIndex(),":", None))
    for item in p[3].nodo:
        nodo2.add(item)
    p[0] = Nodo(Main(p[3].instruccion,p.lineno(1),find_column(p.slice[1])),nodo2) 
    
def p_pmain2(p):
    'pmain : MAIN DOSPUNTOS empty '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pmain-> MAIN DOSPUNTOS epsilon")
    gramatical.add("pmain.val = Main(epsilon)")
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("instruccion-> pmain")
    gramatical.add("instrucion.val = pmain.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo2 = NodoG(getIndex(),"pmain",[])
    nodo2.add(NodoG(getIndex(),"main", None))
    nodo2.add(NodoG(getIndex(),":", None))
    p[0] = Nodo(Main(Vacio(),p.lineno(1),find_column(p.slice[1])),nodo2)


def p_petiqueta(p):
    'petiqueta : ID DOSPUNTOS sentencias'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("petiqueta-> ID DOSPUNTOS sentencias")
    gramatical.add("petiqueta.val = Etiqueta({0},sentencias.val)".format(p[1]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("instruccion-> petiqueta")
    gramatical.add("instrucion.val = petiqueta.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo2 = NodoG(getIndex(),"petiqueta",[])
    nodo2.add(NodoG(getIndex(),p[1], None))
    nodo2.add(NodoG(getIndex(),":", None))
    for item in p[3].nodo:
        nodo2.add(item)
    p[0] = Nodo(Etiqueta(p[1],p[3].instruccion,p.lineno(1),find_column(p.slice[1])),nodo2)


def p_petiqueta2(p):
    'petiqueta : ID DOSPUNTOS empty '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("petiqueta-> ID DOSPUNTOS epsilon")
    gramatical.add("petiqueta.val = Etiqueta({0},epsilon)".format(p[1]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("instruccion-> petiqueta")
    gramatical.add("instrucion.val = petiqueta.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo2 = NodoG(getIndex(),"petiqueta",[])
    nodo2.add(NodoG(getIndex(),p[1], None))
    nodo2.add(NodoG(getIndex(),":", None))
    p[0] = Nodo(Etiqueta(p[1],Vacio(),p.lineno(1),find_column(p.slice[1])),nodo2)


def p_empty(p):
    'empty :'
    pass

def p_sentencias(p):
    'sentencias    :   sentencias sentencia'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("sentencias-> sentencias1 sentencia")
    gramatical.add("sentencias1.val.append(sentencia)")
    gramatical.add("sentencias.val = sentencias1.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[1].instruccion.append(p[2].instruccion)
    nodo2 = NodoG(getIndex(),"sentencia",[])
    nodo2.add(p[2].nodo)
    p[1].nodo.append(nodo2)
    nodo = NodoG(getIndex(),"sentencias",p[1].nodo)
    p[0] = Nodo(p[1].instruccion,[nodo])

def p_sentencias2(p):
    'sentencias    :   sentencia'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("sentencias-> sentencia")
    gramatical.add("sent = []")
    gramatical.add("sent.append(sentencia)")
    gramatical.add("sentencias.val = sent")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    arreglo = []
    arreglo.append(p[1].instruccion)
    p[0]= Nodo(arreglo,[NodoG(getIndex(),"sentencia",[p[1].nodo])])


def p_sentencia(p):
    '''sentencia    : pvariable
                    | preferencia
                    | pgoto
                    | pexit
                    | punset
                    | pif
                    | pprint
                    | pread
                    | parreglo
                    | parray
    '''
    p[0] = p[1]


def p_array(p):
    'parray :   VARIABLE IGUAL ARRAY PARIZQ PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("parray-> VARIABLE IGUAL ARRAY PARIZQ PARDER PYCOMA")
    gramatical.add("parray.val = DeclararArreglo({0})".format(p[1]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> parray")
    gramatical.add("sentencia.val = parray.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"parray",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(NodoG(getIndex(),"array()", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(DeclararArreglo(p[1],p.lineno(1),find_column(p.slice[1])),nodo)

def p_pvariable(p):
    'pvariable : VARIABLE IGUAL operacion PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pvariable-> VARIABLE IGUAL operacion PYCOMA")
    gramatical.add("pvariable.val = Asignacion({0},operacion.val)".format(p[1]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> pvariable")
    gramatical.add("sentencia.val = pvariable.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pvariable",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(p[3].nodo)
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(Asignacion(p[1],p[3].instruccion,Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1])),nodo)
    

def p_arreglo(p):
    'parreglo   :   VARIABLE dimensiones IGUAL operacion PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("parreglo-> VARIABLE dimensiones IGUAL operacion PYCOMA")
    gramatical.add("pvariable.val = Asignacion({0},operacion.val)".format(p[1]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> parreglo")
    gramatical.add("sentencia.val = parreglo.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pvariable",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    for item in p[2].nodo:
        nodo.add(item)
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(p[4].nodo)
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(AsignacionArreglo(p[1],p[2].instruccion,p[4].instruccion,p.lineno(1),find_column(p.slice[1])),nodo)

def p_dimensiones(p):
    'dimensiones    :   dimensiones dimension'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("dimensiones-> dimensiones1 dimension")
    gramatical.add("dimensiones1.val.append(dimension)")
    gramatical.add("dimensiones.val = dimensiones1.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[1].instruccion.append(p[2].instruccion)
    nodo2 = NodoG(getIndex(),"dimension",[])
    nodo2.add(p[2].nodo)
    p[1].nodo.append(nodo2)
    nodo = NodoG(getIndex(),"dimensiones",p[1].nodo)
    p[0] = Nodo(p[1].instruccion,[nodo])

def p_dimensiones2(p):
    'dimensiones    :   dimension'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("dimensiones-> dimension")
    gramatical.add("dime = []")
    gramatical.add("dime.append(dimension)")
    gramatical.add("dimensiones.val = dime")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    arreglo = []
    arreglo.append(p[1].instruccion)
    p[0]= Nodo(arreglo,[NodoG(getIndex(),"dimension",[p[1].nodo])])

def p_dimension(p):
    'dimension  :   CORIZQ valor CORDER'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("dimension-> CORIZQ valor CORDER")
    gramatical.add("dimension.val = valor.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[0] = p[2]

def p_prefencia(p):
    'preferencia    :  VARIABLE IGUAL ANDBIT VARIABLE PYCOMA '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("preferencia-> VARIABLE IGUAL ANDBIT VARIABLE PYCOMA ")
    gramatical.add("preferencia.val = Referencia({0},OperacionVariable({1}))".format(p[1],p[4]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> preferencia")
    gramatical.add("sentencia.val = preferencia.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"preferencia",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(NodoG(getIndex(),"&", None))
    nodo.add(NodoG(getIndex(),p[4], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(Referencia(p[1],OperacionVariable(p[4],p.lineno(4),find_column(p.slice[4])),Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1])),nodo)

def p_pgoto(p):
    'pgoto  :   GOTO ID PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pgoto-> GOTO ID PYCOMA")
    gramatical.add("pgoto.val = Goto({0})".format(p[2]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> pgoto")
    gramatical.add("sentencia.val = pgoto.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pgoto",[])
    nodo.add(NodoG(getIndex(),"goto", None))
    nodo.add(NodoG(getIndex(),p[2], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(Goto(p[2],p.lineno(1),find_column(p.slice[1])), nodo)

def p_psalir(p):
    'pexit  :   EXIT PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pexit-> EXIT PYCOMA")
    gramatical.add("pexit.val = Exit()")
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> pexit")
    gramatical.add("sentencia.val = pexit.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pexit",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(Exit(p.lineno(1),find_column(p.slice[1])), nodo)
    
def p_punset(p):
    'punset  :   UNSET PARIZQ VARIABLE PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("punset-> UNSET PARIZQ VARIABLE PARDER PYCOMA")
    gramatical.add("punset.val = unset({0})".format(p[3]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> punset")
    gramatical.add("sentencia.val = punset.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"punset",[])
    nodo.add(NodoG(getIndex(),"unset", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(NodoG(getIndex(),p[3], None))
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(UnSet(p[3],p.lineno(1),find_column(p.slice[1])), nodo)
    
def p_pif(p):
    'pif    :   IF PARIZQ operacion PARDER GOTO ID PYCOMA '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pif-> IF PARIZQ operacion PARDER GOTO ID PYCOMA")
    gramatical.add("pif.val = If_(operacion.val,goto({0}))".format(p[6]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> pif")
    gramatical.add("sentencia.val = pif.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pif",[])
    nodo.add(NodoG(getIndex(),"if", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(p[3].nodo)
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),"got", None))
    nodo.add(NodoG(getIndex(),p[6], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(If_(p[3].instruccion,Goto(p[6],p.lineno(1),find_column(p.slice[1])),p.lineno(1),find_column(p.slice[1])), nodo)



def p_pprint3(p):
    'pprint :  PRINT PARIZQ VARIABLE dimensiones PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pprint-> PRINT PARIZQ VARIABLE dimensiones PARDER PYCOMA")
    gramatical.add("pprint.val = Print_(OperacionArreglo({0},dimensiones.val))".format(p[3]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> pprint")
    gramatical.add("sentencia.val = pprint.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pprint",[])
    nodo.add(NodoG(getIndex(),"print", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo2 = NodoG(getIndex(),"operacion",[])
    nodo2.add(NodoG(getIndex(),p[3], None))
    for item in p[4].nodo:
        nodo2.add(item)
    nodo.add(nodo2)
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0]=Nodo(Print_(OperacionArreglo(p[3],p[4].instruccion,p.lineno(3),find_column(p.slice[3])),p.lineno(3),find_column(p.slice[3])),nodo)



def p_pprint2(p):
    '''pprint   :   PRINT PARIZQ valor PARDER PYCOMA
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pprint-> PRINT PARIZQ valor PARDER PYCOMA")
    gramatical.add("pprint.val = Print_(Nueva linea)")
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> pprint")
    gramatical.add("sentencia.val = pprint.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pprint",[])
    nodo.add(NodoG(getIndex(),"print", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(p[3].nodo)
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(Print_(p[3].instruccion, p.lineno(1),find_column(p.slice[1])), nodo)

def p_pread(p):
    'pread  :   VARIABLE IGUAL READ PARIZQ PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pread-> VARIABLE IGUAL READ PARIZQ PARDER PYCOMA")
    gramatical.add("pread.val = Read(Asignacion({0}))".format(p[1]))
    lstGrmaticales.append(gramatical)
    gramatical = NodoGramatical("sentencia-> pread")
    gramatical.add("sentencia.val = pread.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"pread",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(NodoG(getIndex(),"read", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(Read(Asignacion(p[1],None,Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1])),p.lineno(1),find_column(p.slice[1])), nodo)


def p_operaciones(p):
    ''' operacion   :   valor MAS valor
                    |   valor MENOS valor
                    |   valor MULTIPLICACION valor
                    |   valor DIVISION valor
                    |   valor MODULAR valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(p[1].nodo)
    nodo.add(NodoG(getIndex(),p[2], None))
    nodo.add(p[3].nodo)

    if p[2] == '+':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MAS valor")
        gramatical.add("operacion.val = OperacionNumerica(valor.val,valor.val, +)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionNumerica(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.SUMA,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '-':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MENOS valor")
        gramatical.add("operacion.val = OperacionNumerica(valor.val,valor.val, -)")
        lstGrmaticales.append(gramatical)
        p[0] = Nodo(OperacionNumerica(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.RESTA,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '*':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MULTIPLICACION valor")
        gramatical.add("operacion.val = OperacionNumerica(valor.val,valor.val, *)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionNumerica(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.MULTIPLICACION,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '/':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor DIVISION valor")
        gramatical.add("operacion.val = OperacionNumerica(valor.val,valor.val, /)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionNumerica(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.DIVISION,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '%':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MODULAR valor")
        gramatical.add("operacion.val = OperacionNumerica(valor.val,valor.val, %)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionNumerica(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.MODULAR,p.lineno(2),find_column(p.slice[2])),nodo)

def p_operaciones2(p):
    ''' operacion   :   NOT valor
                    |   NOTBIT valor
                    |   MENOS valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(p[2].nodo)

    if p[1] == '!':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> NOT valor")
        gramatical.add("operacion.val = OperacionUnaria(valor.val,NOT)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionUnaria(p[2].instruccion,OPERACION_LOGICA.NOT,p.lineno(1),find_column(p.slice[1])),nodo)
    elif p[1] == '~':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> NOTBIT valor")
        gramatical.add("operacion.val = OperacionUnaria(valor.val,NOTBIT)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionUnaria(p[2].instruccion,OPERACION_BIT.NOT,p.lineno(1),find_column(p.slice[1])),nodo)
    elif p[1] == '-':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> MENOS valor")
        gramatical.add("operacion.val = OperacionUnaria(valor.val,RESTA)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER 
        p[0] = Nodo(OperacionUnaria(p[2].instruccion,OPERACION_NUMERICA.RESTA,p.lineno(1),find_column(p.slice[1])),nodo)


def p_operaciones3(p):
    ''' operacion   :   valor AND valor
                    |   valor OR valor
                    |   valor XOR valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(p[1].nodo)
    nodo.add(NodoG(getIndex(),p[2], None))
    nodo.add(p[3].nodo)

    if p[2] == '&&':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor AND valor")
        gramatical.add("operacion.val = OperacionLogica(valor.val,valor.val,AND)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionLogica(p[1].instruccion,p[3].instruccion,OPERACION_LOGICA.AND,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '||':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor OR valor")
        gramatical.add("operacion.val = OperacionLogica(valor.val,valor.val,OR)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionLogica(p[1].instruccion,p[3].instruccion,OPERACION_LOGICA.OR,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == 'xor':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor XOR valor")
        gramatical.add("operacion.val = OperacionLogica(valor.val,valor.val,XOR)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionLogica(p[1].instruccion,p[3].instruccion,OPERACION_LOGICA.XOR,p.lineno(2),find_column(p.slice[2])),nodo)

def p_operaciones4(p):
    ''' operacion   :   valor IGUALIGUAL valor
                    |   valor DIFERENTE valor
                    |   valor MAYOR valor
                    |   valor MENOR valor
                    |   valor MAYORIGUAL valor
                    |   valor MENORIGUAL valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(p[1].nodo)
    nodo.add(NodoG(getIndex(),p[2], None))
    nodo.add(p[3].nodo)

    if p[2] == '==':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor IGUALIGUAL valor")
        gramatical.add("operacion.val = OperacionRelacional(valor.val,valor.val,IGUALIGUAL)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionRelacional(p[1].instruccion,p[3].instruccion,OPERACION_RELACIONAL.IGUAL,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '!=':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor DIFERENTE valor")
        gramatical.add("operacion.val = OperacionRelacional(valor.val,valor.val,DIFERENTE)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionRelacional(p[1].instruccion,p[3].instruccion,OPERACION_RELACIONAL.DIFERENTE,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '>=':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MAYORIGUAL valor")
        gramatical.add("operacion.val = OperacionRelacional(valor.val,valor.val,MAYORIGUAL)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionRelacional(p[1].instruccion,p[3].instruccion,OPERACION_RELACIONAL.MAYORQUE,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '<=':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MENORIGUAL valor")
        gramatical.add("operacion.val = OperacionRelacional(valor.val,valor.val,MENORIGUAL)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionRelacional(p[1].instruccion,p[3].instruccion,OPERACION_RELACIONAL.MENOR,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '>':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MAYOR valor")
        gramatical.add("operacion.val = OperacionRelacional(valor.val,valor.val,MAYOR)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionRelacional(p[1].instruccion,p[3].instruccion,OPERACION_RELACIONAL.MAYOR,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '<':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor MENOR valor")
        gramatical.add("operacion.val = OperacionRelacional(valor.val,valor.val,MENOR)")
        lstGrmaticales.append(gramatical)
        #Parte para AST y GRAFO DE PARSER
        p[0] = Nodo(OperacionRelacional(p[1].instruccion,p[3].instruccion,OPERACION_RELACIONAL.MENOR,p.lineno(2),find_column(p.slice[2])),nodo)


def p_operaciones5(p):
    'operacion  :   ABS PARIZQ valor PARDER'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> ABS PARIZQ valor PARDER")
    gramatical.add("operacion.val = OperacionUnaria(valor.val,ABSOLUTO)")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),"abs", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(p[3].nodo)
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(OperacionUnaria(p[3].instruccion,OPERACION_NUMERICA.ABSOLUTO,p.lineno(1),find_column(p.slice[1])),nodo)

def p_operaciones6(p):
    'operacion  :   ABS PARIZQ MENOS valor PARDER'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> ABS PARIZQ MENOS valor PARDER")
    gramatical.add("operacion.val = OperacionUnaria(valor.val,ABSOLUTO)")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),"abs", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(NodoG(getIndex(),"-", None))
    nodo.add(p[4].nodo)
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(OperacionUnaria(p[4].instruccion,OPERACION_NUMERICA.ABSOLUTO,p.lineno(1),find_column(p.slice[1])),nodo)

def p_operacion7(p):
    'operacion  :   VARIABLE dimensiones'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> VARIABLE dimensiones")
    gramatical.add("operacion.val = OperacionArreglo({0},dimensiones.val)".format(p[1]))
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    for item in p[2].nodo:
        nodo.add(item)
    p[0]=Nodo(OperacionArreglo(p[1],p[2].instruccion,p.lineno(1),find_column(p.slice[1])),nodo)

def p_operacion(p):
    ' operacion     :   valor '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> valor")
    gramatical.add("operacion.val = valor.val")
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"operacion",[p[1].nodo])
    
    p[0]=Nodo(p[1].instruccion,nodo)

def p_operacion8(p):
    '''operacion    :   PARIZQ INTEGER PARDER valor
                    |   PARIZQ FLOAT PARDER valor
                    |   PARIZQ CHAR PARDER valor
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> PARIZQ {0} PARDER valor".format(p[2]))
    gramatical.add("operacion.val = OperacionCasteo({0},valor.val)".format(p[2]))
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),"(",None))
    nodo.add(NodoG(getIndex(),p[2],None))
    nodo.add(NodoG(getIndex(),")",None))
    nodo.add(p[4].nodo)
    p[0] = Nodo(OperacionCasteo(p[2],p[4].instruccion,p.lineno(1),find_column(p.slice[1])),nodo)

def p_operaciones9(p):
    ''' operacion   :   valor ANDBIT valor
                    |   valor ORBIT valor
                    |   valor XORBIT valor
                    |   valor SHIFTIZQ valor
                    |   valor SHIFTDER valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(p[1].nodo)
    nodo.add(NodoG(getIndex(),p[2], None))
    nodo.add(p[3].nodo)
    if p[2] == '&':
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor AND valor")
        gramatical.add("operacion.val = OperacionBit(valor.val,valor.val,AND)".format(p[2]))
        lstGrmaticales.append(gramatical)
        p[0] = Nodo(OperacionBit(p[1].instruccion,p[3].instruccion,OPERACION_BIT.AND,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '|': 
        p[0] = Nodo(OperacionBit(p[1].instruccion,p[3].instruccion,OPERACION_BIT.OR,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '^': 
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor {0} valor".format(p[2]))
        gramatical.add("operacion.val = OperacionBit(valor.val,valor.val,{0})".format(p[2]))
        lstGrmaticales.append(gramatical)
        p[0] = Nodo(OperacionBit(p[1].instruccion,p[3].instruccion,OPERACION_BIT.XOR,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '<<': 
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor SHIFTIZQ valor")
        gramatical.add("operacion.val = OperacionBit(valor.val,valor.val,SHIFTIZQ)".format(p[2]))
        lstGrmaticales.append(gramatical)
        p[0] = Nodo(OperacionBit(p[1].instruccion,p[3].instruccion,OPERACION_BIT.SHIFTIZQ,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '>>': 
        #Parte para reporte Gramatical
        gramatical = NodoGramatical("operacion-> valor SHIFTDER valor")
        gramatical.add("operacion.val = OperacionBit(valor.val,valor.val,SHIFTDER)".format(p[2]))
        lstGrmaticales.append(gramatical)
        p[0] = Nodo(OperacionBit(p[1].instruccion,p[3].instruccion,OPERACION_BIT.SHIFTDER,p.lineno(2),find_column(p.slice[2])),nodo)


def p_valor(p):
    '''valor    :   ENTERO
                |   DECIMAL
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> Entero")
    gramatical.add("operacion.val = OperacionNumero({0})".format(p[1]))
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[0] = Nodo(OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1])),NodoG(getIndex(),str(p[1]), None))

def p_valor2(p):
    '''valor    :   CADENA
                |   CADENA2
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> CADENA")
    gramatical.add("operacion.val = OperacionCadena({0})".format(p[1]))
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[0] = Nodo(OperacionCadena(p[1],p.lineno(1),find_column(p.slice[1])),NodoG(getIndex(),str(p[1]), None))

def p_valor3(p):
    '''valor    :   VARIABLE
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> VARIABLE")
    gramatical.add("operacion.val = OperacionCopiaVariable({0})".format(p[1]))
    lstGrmaticales.append(gramatical)
    #Parte para AST y GRAFO DE PARSER
    p[0] = Nodo(OperacionCopiaVariable(p[1],p.lineno(1),find_column(p.slice[1])),NodoG(getIndex(),str(p[1]), None))

def p_error(p):
    global input
    global parser
    agregarError("Sintactico","Sintaxis no reconocida \"{0}\"".format(p.value),p.lineno+1, find_column(p))

    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'PYCOMA': 
            break
    parser.errok()

    return tok
 
parser = yacc.yacc(write_tables=False)
input = ""
def parse(inpu) :
    global index
    global parser
    global input
    lexer = lex.lex()
    lexer.lineno=0
    input = inpu
    index = 0
    return parser.parse(inpu, lexer=lexer)

def restart():
    global parser
    parser.restart()

def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
