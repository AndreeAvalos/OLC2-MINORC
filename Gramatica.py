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
    'auto':'AUTO',
    'break': 'BREAK',
    'for': 'FOR',
    'case': 'CASE',
    'const':'CONST',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'do':'DO',
    'while':'WHILE',
    'else': 'ELSE',
    'if':'IF',
    'return':'RETURN',
    'sizeof':'SIZE',
    'switch': 'SWITCH',
    'void':'VOID',
    'register': 'REGISTER',
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
    print("Illegal character '%s'" % t.value[0])
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

def p_init(p):
    'init   :   instrucciones'
    p[0] = p[1]

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
                    |   asignacion
                    |   main
                    |   metodo
                    |   funcion
                    |   struct
                    |   error PYCOMA
                    |   error LLAVEDER
    '''
    p[0] = p[1]

def p_declaracion(p):
    'declaracion    :   tipo declaraciones PYCOMA'
    p[0] = Declaraciones(p[1],p[2])

def p_declaraciones(p):
    'declaraciones  :   declaraciones COMA decla'
    p[1].append(p[3])
    p[0] = p[1]

def p_declaraciones2(p):
    'declaraciones  :   decla'
    p[0] = [p[1]]

def p_declaracion2(p):
    'decla          :   ID IGUAL operacion'
    p[0] = Declaracion(p[1],p[3],p.lineno(1),find_column(p.slice[1]))

def p_declaracion3(p):
    'decla          :   ID '
    p[0] = Declaracion(p[1],None,p.lineno(1),find_column(p.slice[1]))

def p_declaracion4(p):
    'declaracion  :   STRUCT ID declaraciones PYCOMA'
    p[0] = DeclaracionesStruct(p[2],p[3])


def p_main(p):
    'main   :   INTEGER MAIN PARIZQ PARDER LLAVEIZQ sentencias LLAVEDER'
    p[0] = Main(p[6])

#falta implementar si el metodo es puntero o doble puntero
def p_metodo(p):
    'metodo :   VOID ID PARIZQ PARDER LLAVEIZQ sentencias LLAVEDER'
    p[0] = Metodo(p[2],None,p[6])

def p_metodo_params(p):
    'metodo :   VOID ID PARIZQ parametros PARDER LLAVEIZQ sentencias LLAVEDER'
    p[0] = Metodo(p[2],p[4],p[7])

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
    p[0] = Funcion(p[1],p[2],None,p[6])

def p_funcion_params(p):
    'funcion :   tipo ID PARIZQ parametros PARDER LLAVEIZQ sentencias LLAVEDER'
    p[0] = Funcion(p[1],p[2],p[4],p[7])

def p_struct(p):
    'struct :   STRUCT ID LLAVEIZQ sdeclaraciones LLAVEDER  PYCOMA'
    p[0] = Struct(p[2],p[4])

def p_sdeclaraciones(p):
    'sdeclaraciones : sdeclaraciones declaracion'
    p[1].append(p[2])

def p_sdeclaraciones2(p):
    'sdeclaraciones :  declaracion'
    p[0] = [p[1]]


def p_sentencias(p):
    'sentencias : sentencias sentencia'
    p[1].append(p[2])
    p[0]=p[1]


def p_sentencias2(p):
    'sentencias : sentencia'
    p[0] = [p[1]]

def p_sentencia(p):
    '''sentencia    :   declaracion
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
                    |   error PYCOMA
                    |   error LLAVEDER
    '''
    p[0] = p[1]

#aqui puede venir tambien tipos de arreglos, structs pero para comenzar una asignacion simple
def p_asignacion(p):
    'asignacion     :   ID IGUAL operacion PYCOMA'
    p[0] = AsignacionSimple(p[1], p[3])

def p_asignacion2(p):
    'asignacion     :   ID tipo_asignacion PYCOMA'
    p[0] = AsignacionCompuesta(p[1],p[2].operadorIzq,p[2].operacion)

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
    p[0] = OperacionAsignacion(p[1],p[2])

def p_asignacion3(p):
    'asignacion :   ID PUNTO atributos IGUAL operacion PYCOMA'
    p[0] = AsignacionStruct(p[1],p[3],p[5])

def p_atributos(p):
    'atributos  : atributos PUNTO ID '
    p[1].append(p[3])
    p[0] = p[1]

def p_atributos2(p):
    'atributos  :   ID'
    p[0] = [p[1]]

#if simple
def p_if(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER'
    s_if = SentenciaIf(p[3],p[6])
    p[0] = If(s_if,None,None)
#if con else simple
def p_if_else(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER ELSE LLAVEIZQ sentencias LLAVEDER'
    s_if = SentenciaIf(p[3],p[6])
    s_else = SentenciaIf(None,p[10])
    p[0] = If(s_if,None,s_else)
#if con else if pero sin else
def p_if_elseif(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER else_if'
    s_if = SentenciaIf(p[3],p[6])
    s_elif = p[8]
    p[0] = If(s_if,s_elif,None)

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
    p[0] = SentenciaIf(p[4],p[7])

#if con elseif y else
def p_if_elseif_else(p):
    'if :   IF PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER else_if ELSE LLAVEIZQ sentencias LLAVEDER'
    s_if = SentenciaIf(p[3],p[6])
    s_elif = p[8]
    s_else = SentenciaIf(None,p[11])
    p[0] = If(s_if,s_elif,s_else)

def p_while(p):
    'while  :   WHILE PARIZQ operacion PARDER LLAVEIZQ sentencias LLAVEDER'
    p[0]= While(p[3],p[6])

def p_do_while(p):
    'do_while   :   DO LLAVEIZQ sentencias LLAVEDER WHILE PARIZQ operacion PARDER PYCOMA '
    p[0] = DoWhile(p[7],p[3])

def p_for(p):
    'for    :   FOR PARIZQ inicializacion PYCOMA operacion PYCOMA incremento PARDER LLAVEIZQ sentencias LLAVEDER'

def p_inicializacion(p):
    'inicializacion :   tipo ID IGUAL operacion '

def p_inicializacion2(p):
    'inicializacion :   ID IGUAL operacion '

def p_incremento(p):
    'incremento :   ID MAS MAS '
def p_incremento2(p):
    'incremento :   ID MENOS MENOS'
def p_incremento(p):
    'incremento :   ID tipo_asignacion '
def p_callMetodo(p):
    'callMetodo :   ID PARIZQ PARDER PYCOMA'
    p[0] = Llamada(p[1],None)

def p_callMetodo2(p):
    'callMetodo :   ID PARIZQ valores PARDER PYCOMA'
    p[0] = Llamada(p[1],p[3])

def p_print(p):
    'print  :   PRINT PARIZQ CADENA COMA valores PARDER PYCOMA'
    p[0] = Print(p[3],p[5])

def p_print2(p):
    'print  :   PRINT PARIZQ CADENA PARDER PYCOMA'
    p[0] = Print(p[3],None)

def p_valores(p):
    'valores    :   valores COMA operacion'
    p[1].append(p[3])
    p[0] = p[1]

def p_valores2(p):
    'valores    :   operacion'
    p[0] = [p[1]]

def p_switch(p):
    'switch :   SWITCH PARIZQ operacion PARDER LLAVEIZQ casos LLAVEDER'
    p[0]= Switch(p[3],p[6])

def p_casos(p):
    'casos  :   casos caso'
    p[1].append(p[2])
    p[0]=p[1]

def p_casos2(p):
    'casos  :   caso'
    p[0] = [p[1]]

def p_caso(p):
    'caso   :   CASE operacion DOSPUNTOS sentencias'
    p[0] = Case(p[2],p[4])

def p_caso2(p):
    'caso   :   DEFAULT DOSPUNTOS sentencias'
    p[0] = Case(None, p[3])

def p_break(p):
    'break  :   BREAK PYCOMA'
    p[0] = Break()

def p_return(p):
    'return :   RETURN operacion PYCOMA'
    p[0] = Return(p[2])

def p_operaciones_logicas(p):
    '''operacion    :   operacion   AND             operacion
                    |   operacion   OR              operacion 
    '''
    p[0] = OperacionBinaria(p[1],p[3],p[2],p.lineno(2),find_column(p.slice[2]))

def p_operaciones_relacionales(p):
    '''operacion    :   operacion   IGUALIGUAL      operacion
                    |   operacion   DIFERENTE       operacion 
                    |   operacion   MAYOR           operacion
                    |   operacion   MENOR           operacion
                    |   operacion   MAYORIGUAL      operacion
                    |   operacion   MENORIGUAL      operacion
    '''
    p[0] = OperacionBinaria(p[1],p[3],p[2],p.lineno(2),find_column(p.slice[2]))

def p_operaciones_bit(p):
    '''operacion    :   operacion   ANDBIT          operacion
                    |   operacion   ORBIT           operacion 
                    |   operacion   XORBIT          operacion
                    |   operacion   SHIFTIZQ        operacion
                    |   operacion   SHIFTDER        operacion
    '''
    p[0] = OperacionBinaria(p[1],p[3],p[2],p.lineno(2),find_column(p.slice[2]))

def p_operaciones_numerica(p):
    '''operacion    :   operacion   MAS             operacion
                    |   operacion   MENOS           operacion
                    |   operacion   MULTIPLICACION  operacion
                    |   operacion   DIVISION        operacion
                    |   operacion   MODULAR         operacion
    '''
    p[0] = OperacionBinaria(p[1],p[3],p[2],p.lineno(2),find_column(p.slice[2]))

def p_operaciones_ternario(p):
    'operacion      :   operacion   INTERROGACION operacion DOSPUNTOS operacion'
    p[0] = OperacionTernaria(p[1], p[3],p[4],p.lineno(2),find_column(p.slice[2]))

def p_operaciones_unarias(p):
    '''operacion    :   MENOS   operacion   %prec UMENOS
                    |   NOT     operacion   %prec UMENOS
                    |   NOTBIT  operacion   %prec UMENOS
    '''
    p[0] = OperacionUnaria(p[2], p[1],p.lineno(1),find_column(p.slice[1]))

def p_operaciones_funcion(p):
    'operacion :   ID PARIZQ PARDER'
    p[0] = OperacionLlamada(p[1],None)

def p_operaciones_funcion2(p):
    'operacion :   ID PARIZQ valores PARDER'
    p[0] = OperacionLlamada(p[1],p[3])

def p_operacion_struct(p):
    'operacion  : ID PUNTO atributos'
    p[0] = OperacionStruct(p[1],p[3])

def p_operacion_scan(p):
    'operacion  :   SCAN PARIZQ PARDER'
    p[0] = Scan()

def p_operaciones_valor(p):
    'operacion      :   valor'
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
    p[0] = OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1]))
def p_valor_identificador(p):
    'valor          : ID'
    p[0] = OperacionVariable(p[1],p.lineno(1),find_column(p.slice[1]))
def p_valor_double(p):
    'valor          : DECIMAL'
    p[0] = OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1]))
def p_valor_char(p):
    'valor          : CARACTER'   
    p[0] = OperacionCaracter(p[1],p.lineno(1),find_column(p.slice[1]))
def p_valor_cadena(p):
    'valor          : CADENA'  
    p[0] = OperacionCadena(p[1],p.lineno(1),find_column(p.slice[1])) 

def p_error(p):
    print("Error sintáctico en '%s'" % p.value, str(p.lineno))



input = ""
parser = yacc.yacc(write_tables=False)
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