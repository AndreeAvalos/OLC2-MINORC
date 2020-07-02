import ply.yacc as yacc
import ply.lex as lex
from Instruccion import *


reservadas = {
    'int': 'INTEGER',
    'float': 'FLOAT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'main': 'MAIN',
    'printf': 'PRINT',
    'struct': 'STRUCT',
    'break': 'BREAK',
    'for': 'FOR',
    'case': 'CASE',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'do':'DO',
    'while':'WHILE',
    'else': 'ELSE',
    'if':'IF',
    'return':'RETURN',
    'switch': 'SWITCH',
    'void':'VOID',
    'goto': 'GOTO',
    'scanf': 'SCAN'
}

tokens = [
    'PYCOMA',
    'PUNTO',
    'INTERROGACION',
    'COMA',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAVEIZQ',
    'LLAVEDER',
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
    'CARACTER',
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
    'MASIGUAL',
    'MENOSIGUAL',
    'ASTERISCOIGUAL',
    'BARRAIGUAL',
    'MODULARIGUAL',
    'ANDIGUAL',
    'XORIGUAL',
    'ORIGUAL',
    'SHIFTDERIGUAL',
    'SHIFTIZQIGUAL',
    'INCREMENTO',
    'DECREMENTO'

] + list(reservadas.values())

t_PYCOMA = r';'
t_PUNTO = r'\.'
t_INTERROGACION = r'\?'
t_COMA = r','
t_DOSPUNTOS = r':'
t_LLAVEIZQ = r'{'
t_LLAVEDER = r'}'
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
t_MASIGUAL = r'\+='
t_MENOSIGUAL = r'-='
t_ASTERISCOIGUAL = r'\*='
t_BARRAIGUAL = r'/='
t_MODULARIGUAL = r'%='
t_SHIFTIZQIGUAL = r'<<='
t_SHIFTDERIGUAL = r'>>='
t_ANDIGUAL = r'&='
t_ORIGUAL = r'\|='
t_XORIGUAL = r'\^='
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'

#t_ESCAPE =r'\"\\n\"'

t_ignore = " \t\r"

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

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CARACTER(t):
    r'\'.\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1


def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    #editar para agregar a una tabla
    #print("Illegal character \"{0}\" linea: {1}".format(t.value[0],t.lexer.lineno+1))
    #agregarError('Lexico',"Caracter \'{0}\' ilegal".format(t.value[0]), t.lexer.lineno+1,find_column(t))
    t.lexer.skip(1)



precedence = (
    ('left', 'COMA'),
    ('right','IGUAL','ASTERISCOIGUAL','BARRAIGUAL', 'MODULARIGUAL', 
        'MASIGUAL', 'MENOSIGUAL', 'SHIFTDERIGUAL',
        'SHIFTIZQIGUAL', 'ANDIGUAL', 'XORIGUAL', 'ORIGUAL'),
    ('right', 'INTERROGACION'),
    ('left', 'OR',),
    ('left', 'AND'),
    ('left', 'ORBIT',),
    ('left', 'XORBIT',),
    ('left', 'ANDBIT'),
    ('left', 'IGUALIGUAL', 'DIFERENTE'),
    ('left', 'MENOR', 'MENORIGUAL', 'MAYOR','MAYORIGUAL'),
    ('left', 'SHIFTIZQ', 'SHIFTDER'),
    ('left','MAS','MENOS'),
    ('left','MULTIPLICACION','DIVISION', 'MODULAR'),
    ('right','UMENOS'),
    )


nodos = {}
#ejemplo de nodos {"indice: 0, op: a, izq: "", der: "" "}
index = 0 

def getIndex(op, izq, der):
    global index 
    global nodos
    for key in nodos:
        if nodos[key]["op"] == op:
            if nodos[key]["izq"] == izq:
                if nodos[key]["der"] == der:
                    return nodos[key]["indice"]
    index+=1
    nodos[index] = {"indice": index, "op": op, "izq": izq, "der": der}
    return index

def p_init(p):
    'init   :   instrucciones'
    global nodos
    p[0] = nodos

def p_instrucciones(p):
    'instrucciones  :   instrucciones instruccion'
    p[1].append(p[2])
    p[0] = p[1]

def p_instrucciones2(p):
    'instrucciones :    instruccion'
    array = []
    array.append(p[1])
    p[0] = array

def p_instruccion(p):
    '''instruccion  :   declaracion
                    |   declaracion_arreglo
                    |   declaracion_arreglo_struct
                    |   asignacion
                    |   main
                    |   metodo
                    |   funcion
                    |   struct
                    |   declaracion_casteo
                    |   error PYCOMA
                    |   error LLAVEDER
    '''
    p[0] = p[1]


def p_declaracion(p):
    'declaracion    :   tipo declaraciones PYCOMA'

def p_declaraciones(p):
    'declaraciones  :   declaraciones COMA decla'
    p[1].append(p[3])
    p[0] = p[1]

def p_declaraciones2(p):
    'declaraciones  :   decla'
    p[0] = [p[1]]

def p_declaracion2(p):
    'decla          :   ID IGUAL operacion'

def p_declaracion_string(p):
    'decla          :   ID CORIZQ CORDER IGUAL CADENA'

def p_declaracion3(p):
    'decla          :   ID '

def p_declaracion4(p):
    'declaracion    :   STRUCT ID declaraciones PYCOMA'

def p_declaracion_arreglo(p):
    'declaracion_arreglo    :   tipo declaraciones_arreglos PYCOMA'

def p_declaracion_arreglos2(p):
    'declaraciones_arreglos :   declaraciones_arreglos COMA decla_arreglo'
    p[1].append(p[3])
    p[0] = p[1]

def p_declaracion_arreglos3(p):
    'declaraciones_arreglos :   decla_arreglo'  
    p[0] = [p[1]]

def p_declaracion_arreglo2(p):
    'decla_arreglo  :   ID corchetes IGUAL LLAVEIZQ llaves LLAVEDER'

def p_declaracion_arreglo3(p):
    'decla_arreglo  :   ID corchetes'

def p_corchetes(p):
    'corchetes  :   corchetes corchete'
    p[1].append(p[2])
    p[0] = p[1]

def p_corchetes2(p):
    'corchetes  :   corchete'
    p[0] = [p[1]]

def p_corchete(p):
    'corchete   :   CORIZQ operacion CORDER'
    p[0] = p[2]

def p_llaves(p):
    'llaves :   llaves COMA llave'
    p[1].append(p[3])
    p[0] = p[1]

def p_llaves3(p):
    'llaves :   llave'
    p[0] = [p[1]]

def p_llave(p):
    'llave  :   operacion'
    p[0] = p[1]

def p_llaves2(p):
    'llave :   LLAVEIZQ llaves LLAVEDER'
    p[0] = p[2]

def p_declaracion_arreglo_struct(p):
    'declaracion_arreglo_struct : STRUCT ID arreglo_structs PYCOMA'

def p_declaracion_casteo(p):
    'declaracion_casteo :   tipo ID IGUAL PARIZQ primitivo PARDER operacion PYCOMA'
    
def p_asignacion_ternaria2(p):
    'declaracion    : tipo  ID IGUAL operacion INTERROGACION operacion DOSPUNTOS operacion PYCOMA'

def p_arreglo_structs(p):
    'arreglo_structs    :   arreglo_structs COMA arreglo_struct'
    p[1].append(p[3])
    p[0] = p[1]

def p_arreglo_structs2(p):
    'arreglo_structs    :   arreglo_struct'
    p[0] = [p[1]]

def p_arreglo_structs3(p):
    'arreglo_struct     :   ID corchetes'
def p_main(p):
    'main   :   INTEGER MAIN PARIZQ PARDER LLAVEIZQ sentencias LLAVEDER'

#falta implementar si el metodo es puntero o doble puntero
def p_metodo(p):
    'metodo :   VOID ID PARIZQ PARDER LLAVEIZQ sentencias LLAVEDER'

def p_metodo_params(p):
    'metodo :   VOID ID PARIZQ parametros PARDER LLAVEIZQ sentencias LLAVEDER'

def p_parametros(p):
    'parametros :   parametros COMA parametro '
    p[1].append(p[3])
    p[0] = p[1]

def p_parametros2(p):
    'parametros :   parametro   '
    p[0] = [p[1]]

#faltaria los parametros con puntero
def p_parametro(p):
    'parametro  :   tipo ID'
    p[0] = p[2]


def p_funcion(p):
    'funcion :   tipo ID PARIZQ PARDER LLAVEIZQ sentencias LLAVEDER'

def p_funcion_params(p):
    'funcion :   tipo ID PARIZQ parametros PARDER LLAVEIZQ sentencias LLAVEDER'

def p_struct(p):
    'struct :   STRUCT ID LLAVEIZQ sdeclaraciones LLAVEDER  PYCOMA'

def p_sdeclaraciones(p):
    'sdeclaraciones : sdeclaraciones sdeclaracion'
    p[1].append(p[2])
    p[0] = p[1]

def p_sdeclaraciones2(p):
    '''sdeclaraciones   :   sdeclaracion
    '''
    p[0] = [p[1]]

def p_sdeclaracion3(p):
    '''sdeclaracion :   declaracion
                    |   declaracion_arreglo
                    |   declaracion_arreglo_struct
    '''
    p[0]=p[1]

def p_sentencias(p):
    'sentencias : sentencias sentencia'
    p[1].append(p[2])
    p[0]=p[1]


def p_sentencias2(p):
    'sentencias : sentencia'
    p[0] = [p[1]]

def p_sentencia(p):
    '''sentencia    :   declaracion
                    |   declaracion_arreglo
                    |   declaracion_arreglo_struct
                    |   declaracion_casteo
                    |   asignacion 
                    |   if
                    |   while
                    |   for
                    |   do_while
                    |   switch
                    |   break
                    |   return
                    |   callMetodo
                    |   print
                    |   goto
                    |   etiqueta
                    |   continue
                    |   error PYCOMA
                    |   error LLAVEDER
    '''
    p[0] = p[1]

def p_goto(p):
    'goto   :   GOTO ID PYCOMA'

def p_continue(p):
    'continue   :   CONTINUE PYCOMA'

def p_etiqueta(p):
    'etiqueta   :   ID DOSPUNTOS   '

#aqui puede venir tambien tipos de arreglos, structs pero para comenzar una asignacion simple
def p_asignacion(p):
    'asignacion     :   ID IGUAL operacion PYCOMA'

def p_asignacion2(p):
    'asignacion     :   ID tipo_asignacion PYCOMA'

def p_tipo_asignacion(p):
    '''tipo_asignacion  :      MASIGUAL        operacion
                        |      MENOSIGUAL      operacion
                        |      ASTERISCOIGUAL  operacion
                        |      BARRAIGUAL      operacion
                        |      MODULARIGUAL    operacion
                        |      SHIFTDERIGUAL   operacion
                        |      SHIFTIZQIGUAL   operacion
                        |      ANDIGUAL        operacion
                        |      ORIGUAL         operacion
                        |      XORIGUAL        operacion
    '''

def p_tipo_asignacion2(p):
    '''tipo_asignacion  :      INCREMENTO
                        |      DECREMENTO
    '''

def p_asignacion3(p):
    'asignacion :   ID PUNTO atributos IGUAL operacion PYCOMA'


def p_atributos(p):
    'atributos  : atributos PUNTO atributo'
    p[1].append(p[3])
    p[0] = p[1]

def p_atributos2(p):
    'atributos  :   atributo'
    p[0] = [p[1]]

def p_atributo(p):
    'atributo   :   ID'

def p_atributo2(p):
    'atributo   :   ID corchetes'
def p_asignacion4(p):
    'asignacion :   ID corchetes IGUAL operacion PYCOMA'

def p_asignacion5(p):
    'asignacion :   ID corchetes PUNTO atributos IGUAL operacion PYCOMA'

def p_asignacion_casteo(p):
    'asignacion :   ID IGUAL PARIZQ primitivo PARDER operacion PYCOMA'

def p_asignacion_ternaria(p):
    'asignacion   :   ID IGUAL operacion INTERROGACION operacion DOSPUNTOS operacion PYCOMA'

#if simple
def p_if(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER'
#if con else simple
def p_if_else(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER ELSE LLAVEIZQ sentencias LLAVEDER'
#if con else if pero sin else
def p_if_elseif(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER else_if'

#listados de if
def p_else_if(p):
    'else_if    :   else_if elif'
    p[1].append(p[2])
    p[0]=p[1]
#un unico else if 
def p_else_if2(p):
    'else_if    :   elif'
    p[0] = [p[1]]

#sentencia else if
def p_elif(p):
    'elif   :   ELSE IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER '

#if con elseif y else
def p_if_elseif_else(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER else_if ELSE LLAVEIZQ sentencias LLAVEDER'

def p_while(p):
    'while  :   WHILE PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER'

def p_do_while(p):
    'do_while   :   DO LLAVEIZQ sentencias LLAVEDER WHILE PARIZQ operacion PARDER PYCOMA '

def p_for(p):
    'for    :   FOR PARIZQ inicializacion PYCOMA operacion PYCOMA incremento PARDER LLAVEIZQ sentencias LLAVEDER'
    
def p_inicializacion(p):
    'inicializacion :   tipo ID IGUAL operacion '

def p_inicializacion2(p):
    'inicializacion :   ID IGUAL operacion '

def p_incremento3(p):
    'incremento :   ID tipo_asignacion '

def p_callMetodo(p):
    'callMetodo :   ID PARIZQ PARDER PYCOMA'

def p_callMetodo2(p):
    'callMetodo :   ID PARIZQ valores PARDER PYCOMA'

def p_print(p):
    'print  :   PRINT PARIZQ CADENA COMA valores PARDER PYCOMA'

def p_print2(p):
    'print  :   PRINT PARIZQ CADENA PARDER PYCOMA'

def p_valores(p):
    'valores    :   valores COMA operacion'
    p[1].append(p[3])
    p[0] = p[1]

def p_valores2(p):
    'valores    :   operacion'
    p[0] = [p[1]]

def p_switch(p):
    'switch :   SWITCH PARIZQ operacion PARDER LLAVEIZQ casos LLAVEDER'

def p_casos(p):
    'casos  :   casos caso'
    p[1].append(p[2])
    p[0]=p[1]

def p_casos2(p):
    'casos  :   caso'
    p[0] = [p[1]]

def p_caso(p):
    'caso   :   CASE operacion DOSPUNTOS sentencias'

def p_caso2(p):
    'caso   :   DEFAULT DOSPUNTOS sentencias'

def p_break(p):
    'break  :   BREAK PYCOMA'

def p_return(p):
    'return :   RETURN operacion PYCOMA'

def p_operaciones_logicas(p):
    '''operacion    :   operacion   AND             operacion
                    |   operacion   OR              operacion 
    '''
    p[0] = getIndex(p[2],p[1],p[3])

def p_operaciones_relacionales(p):
    '''operacion    :   operacion   IGUALIGUAL      operacion
                    |   operacion   DIFERENTE       operacion 
                    |   operacion   MAYOR           operacion
                    |   operacion   MENOR           operacion
                    |   operacion   MAYORIGUAL      operacion
                    |   operacion   MENORIGUAL      operacion
    '''
    p[0] = getIndex(p[2],p[1],p[3])

def p_operaciones_bit(p):
    '''operacion    :   operacion   ANDBIT          operacion
                    |   operacion   ORBIT           operacion 
                    |   operacion   XORBIT          operacion
                    |   operacion   SHIFTIZQ        operacion
                    |   operacion   SHIFTDER        operacion
    '''
    p[0] = getIndex(p[2],p[1],p[3])

def p_operaciones_numerica(p):
    '''operacion    :   operacion   MAS             operacion
                    |   operacion   MENOS           operacion
                    |   operacion   MULTIPLICACION  operacion
                    |   operacion   DIVISION        operacion
                    |   operacion   MODULAR         operacion
    '''
    p[0] = getIndex(p[2],p[1],p[3])

def p_operaciones_unarias(p):
    '''operacion    :   MENOS   operacion   %prec UMENOS
                    |   NOT     operacion   %prec UMENOS
                    |   NOTBIT  operacion   %prec UMENOS
                    |   ANDBIT  operacion   %prec UMENOS
    '''
    p[0] = getIndex(p[1],p[2],"")
   

def p_operaciones_funcion(p):
    'operacion :   ID PARIZQ PARDER'
    p[0] = getIndex(p[1],"","")

def p_operaciones_funcion2(p):
    'operacion :   ID PARIZQ valores PARDER'
    p[0] = getIndex(p[1],"","")

def p_operacion_struct(p):
    'operacion  : ID PUNTO atributos'
    p[0] = getIndex(p[1],"","")

def p_operacion_scan(p):
    'operacion  :   SCAN PARIZQ PARDER'
    p[0] = getIndex(p[1],"","")

def p_operacion_arreglo(p):
    'operacion  :   ID corchetes'
    p[0] = getIndex(p[1],"","")

def p_operacion_arreglo_struct(p):
    'operacion  :   ID corchetes PUNTO atributos'
    p[0] = getIndex(p[1],"","")
    
def p_operaciones_parentesis(p):
    'operacion  :   PARIZQ operacion PARDER'
    p[0] = p[2]

def p_operaciones_valor(p):
    'operacion      :   valor'
    p[0] = p[1]

def p_primitivo(p):
    '''primitivo    :   INTEGER
                    |   FLOAT
                    |   DOUBLE
                    |   CHAR
    '''
    p[0] = p[1]

def p_tipo(p):
    '''tipo         :   INTEGER
                    |   FLOAT
                    |   DOUBLE
                    |   CHAR
                    |   ID
    '''
    p[0] = p[1]

def p_valor_integer(p):
    'valor          : ENTERO'
    p[0] = getIndex(p[1],"","")
    
def p_valor_identificador(p):
    'valor          : ID'
    p[0] = getIndex(p[1],"","")
    
def p_valor_double(p):
    'valor          : DECIMAL'
    p[0] = getIndex(p[1],"","")
   
def p_valor_char(p):
    'valor          : CARACTER'
    p[0] = getIndex(p[1],"","")   
    
def p_valor_cadena(p):
    'valor          : CADENA'
    p[0] = getIndex(p[1],"","")
    

def p_error(p):
    ''

input = ""
parser = yacc.yacc(write_tables=True)
def parse(inpu) :
    global input
    lexer = lex.lex()
    lexer.lineno=0
    index = 0
    input = inpu
    return parser.parse(inpu, lexer=lexer)

def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1