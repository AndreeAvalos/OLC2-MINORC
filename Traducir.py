import threading
import time
from Instruccion import *
from TablaSimbolo import *
from PyQt5 import QtWidgets,QtCore

class Traducir(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)

        self.ast = args[0]
        self.TC = args[1]
        self.C3D = args[2]
        self.ts = TablaSimbolos()
        self.index_temporal = 0
        self.cuadruplos = Cuadruplos()
        self.etiquetas = {}
        self.funciones = {}
        self.structs = {}
        self.etiqueta = "main"
        self.ambito_ejecucion = "main"
        self.last_etiqueta = ""
        self.index_if = 0
        self.index_etiquetas = 0
        self.index_while=0
        self.index_end = 0
        self.index_do = 0
        self.index_heap = 0
        self.index_switch =0 
        self.index_case = 0
        self.index_default = 0
        self.sentencia_break =""


    def run(self):
        self.recolectar(self.ast)
        self.procesar()
        self.imprimirCuadruplos()
        self.imprimir3D()

    def imprimir3D(self):
        for etiqueta in self.etiquetas:
            self.C3D.addItem(etiqueta+":")
            print(etiqueta+":")
            for cuadruplo in self.etiquetas[etiqueta]:
                if cuadruplo.op == "if":
                    self.C3D.addItem(" if({0}) goto {1};".format(cuadruplo.arg1, cuadruplo.result))
                    print(" if({0}) goto {1};".format(cuadruplo.arg1, cuadruplo.result))
                elif cuadruplo.op == "goto":
                    self.C3D.addItem(" goto {0};".format(cuadruplo.arg1))
                    print(" goto {0};".format(cuadruplo.arg1))
                elif cuadruplo.op != "=":
                    self.C3D.addItem(" {0}={1} {2} {3};".format(cuadruplo.result,cuadruplo.arg1, cuadruplo.op, cuadruplo.arg2))
                    print(" {0}={1} {2} {3};".format(cuadruplo.result,cuadruplo.arg1, cuadruplo.op, cuadruplo.arg2))
                else:
                    self.C3D.addItem(" {0}={1}{2};".format(cuadruplo.result,cuadruplo.arg1,cuadruplo.arg2))
                    print(" {0}={1}{2};".format(cuadruplo.result,cuadruplo.arg1,cuadruplo.arg2))
            self.C3D.addItem("")

    def imprimirCuadruplos(self):
        datos = []
        for cuadruplo in self.cuadruplos.cuadruplos:
            datos.append((cuadruplo.op,str(cuadruplo.arg1),str(cuadruplo.arg2),cuadruplo.result))

        for i in range(self.TC.rowCount()):
            self.TC.removeRow(i)
        self.TC.clearContents()

        fila = 0
        for registro in datos:
            columna = 0
            self.TC.insertRow(fila)
            for item in registro:
                celda = QtWidgets.QTableWidgetItem(item)
                self.TC.setItem(fila,columna,celda)
                columna+=1
            fila+=1
    
    def recolectar(self, instrucciones):
        self.etiquetas["main"]=[]
        new_cuadruplo = Cuadruplo("=","array()","","$s1")
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas["main"].insert(0,new_cuadruplo)
        for instruccion in instrucciones:
            if isinstance(instruccion, Declaraciones): self.recolectar_declaraciones(instruccion)
            elif isinstance(instruccion, Main): self.recolectar_main(instruccion)
            elif isinstance(instruccion, Metodo): self.recolectar_metodo(instruccion)
            elif isinstance(instruccion, Funcion): self.recolectar_funcion(instruccion)
            elif isinstance(instruccion, AsignacionSimple): self.procesar_asignacionSimple(instruccion,self.ts)
            elif isinstance(instruccion, AsignacionCompuesta): self.procesar_asignacionCompuesta(instruccion,self.ts)


    def recolectar_main(self, instruccion):
        if not "main" in self.funciones:
            self.funciones["main"] = {"tipo":"void","sentencias":instruccion.sentencias,"params":None}

    def recolectar_metodo(self, instruccion):
        if not instruccion.id in self.funciones:
            self.funciones[instruccion.id] ={"tipo":"void","sentencias":instruccion.sentencias,"params":instruccion.params}

    def recolectar_funcion(self, instruccion):
        if not instruccion.id in self.funciones:
            self.funciones[instruccion.id] ={"tipo":instruccion.tipo,"sentencias":instruccion.sentencias,"params":instruccion.params}

    def recolectar_declaraciones(self,instruccion):
        for instru in instruccion.declaraciones:
            self.recolectar_declaracion(instru)

    def recolectar_declaracion(self, instruccion):
        id = instruccion.id
        if not self.ts.existe(id):
            if instruccion.valor:
                last_temp = self.procesar_operacion(instruccion.valor,self.ts)
                temp = self.generarHeap()
                new_simbol = Simbolo(id, temp, instruccion.line, instruccion.column)
                self.ts.add(new_simbol)
                new_cuadruplo = Cuadruplo("=", last_temp,"",temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            else:
                temp = self.generarHeap()
                new_simbol = Simbolo(id, temp, instruccion.line, instruccion.column)
                self.ts.add(new_simbol)
                new_cuadruplo = Cuadruplo("=", "0","",temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
                
        
    def procesar(self):
        if "main" in self.funciones:
            self.procesar_main(self.funciones["main"]["sentencias"], self.ts)
    
    def procesar_main(self, sentencias, ts):
        self.etiqueta = "main"
        self.ambito_ejecucion = "main"
        new_cuadruplo = Cuadruplo("=","array()","","$s0")
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].insert(0,new_cuadruplo)

        self.procesar_sentencias(sentencias, ts)
        '''local = TablaSimbolos()
        local.setPadre(ts)
        for sentencia in sentencias:
            if isinstance(sentencia,Declaraciones): self.procesar_declaraciones(sentencia,local)
            elif isinstance(sentencia,AsignacionSimple): self.procesar_asignacionSimple(sentencia,local)
            elif isinstance(sentencia,AsignacionCompuesta): self.procesar_asignacionCompuesta(sentencia,local)
            elif isinstance(sentencia,If):  self.procesar_if(sentencia,local)'''

    def procesar_declaraciones(self,instruccion,ts):
        for instru in instruccion.declaraciones:
            self.procesar_declaracion(instru,ts)

    def procesar_declaracion(self, instruccion, ts):
        id = instruccion.id
        if not ts.existe(id):
            if instruccion.valor:
                last_temp = self.procesar_operacion(instruccion.valor,ts)
                temp = self.generarTemporal()
                new_simbol = Simbolo(id, temp, instruccion.line, instruccion.column)
                ts.add(new_simbol)
                new_cuadruplo = Cuadruplo("=", last_temp,"",temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            else:
                temp = self.generarTemporal()
                new_simbol = Simbolo(id, temp, instruccion.line, instruccion.column)
                ts.add(new_simbol)
                new_cuadruplo = Cuadruplo("=", "0","",temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)

    def procesar_asignacionSimple(self, instruccion, ts):
        id = instruccion.id
        if ts.existePadre(id,ts):
            temp = ts.getValor(id, ts).temporal
            last_temp = self.procesar_operacion(instruccion.valor,ts)
            new_cuadruplo = Cuadruplo("=", last_temp,"",temp)
            self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)

    def procesar_asignacionCompuesta(self, instruccion, ts):
        id = instruccion.id
        if ts.existePadre(id,ts):

            temp = self.generarTemporal()
            new_cuadruplo = Cuadruplo("=", ts.getValor(id, ts).temporal,"",temp)
            self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)
            last_temp = self.procesar_operacion(instruccion.operadorIzq,ts)

            operacion = instruccion.operacion
            if operacion == '+=':
                new_cuadruplo = Cuadruplo("+", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '-=':
                new_cuadruplo = Cuadruplo("-", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '*=':
                new_cuadruplo = Cuadruplo("*", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '/=':
                new_cuadruplo = Cuadruplo("/", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '%=':
                new_cuadruplo = Cuadruplo("%", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '&=':
                new_cuadruplo = Cuadruplo("&&", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '|=':
                new_cuadruplo = Cuadruplo("||", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '^=':
                new_cuadruplo = Cuadruplo("xor", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '<<=':
                new_cuadruplo = Cuadruplo("<<", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '>>=':
                new_cuadruplo = Cuadruplo(">>", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)

            new_cuadruplo = Cuadruplo("=",temp,"", ts.getValor(id, ts).temporal)
            self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)

    def procesar_if(self,sentenciaif,ts):
        #operamos toda la condicion del if
        new_etiqueta = self.generarEtiqueta()
        s_if = sentenciaif.s_if
        s_elif = sentenciaif.s_elif
        s_else = sentenciaif.s_else
        last_temp = self.procesar_operacion(s_if.condicion,ts)
        new_if = self.generarIF()
        new_cuadruplo = Cuadruplo("if", last_temp,"goto",new_if)
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        old_etiqueta = self.etiqueta
        self.etiquetas[new_if] = []
        self.etiqueta = new_if
        #ciclo para agregar etiquetas en if generado 
        self.procesar_sentencias(s_if.sentencias,ts)
        #para volver al main
        new_cuadruplo = Cuadruplo("goto",new_etiqueta, "","")
        #self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        self.etiqueta = old_etiqueta
        #ciclo para elseif
        if s_elif:
            for s_if2 in s_elif:
                last_temp = self.procesar_operacion(s_if2.condicion,ts)
                new_if = self.generarIF()
                new_cuadruplo = Cuadruplo("if", last_temp,"goto",new_if)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
                old_etiqueta = self.etiqueta
                self.etiquetas[new_if] = []
                self.etiqueta = new_if
                self.procesar_sentencias(s_if2.sentencias,ts)
                new_cuadruplo = Cuadruplo("goto",new_etiqueta, "","")
                #self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
                self.etiqueta = old_etiqueta
        #else
        if s_else:
            self.etiqueta = old_etiqueta
            self.procesar_sentencias(s_else.sentencias,ts)
        #creamos una nueva etiqueta que nos diriga hacia lo que traia el main
        new_cuadruplo = Cuadruplo("goto",new_etiqueta, "","")
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        self.etiquetas[new_etiqueta] = []
        self.etiqueta = new_etiqueta

    def procesar_while(self,sentenciaWhile, ts):
        new_etiqueta = self.generarEND()
        new_while = self.generarWHILE()
        new_cuadruplo = Cuadruplo("goto",new_while, "","")
        #self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        self.etiquetas[new_while] = []
        old_etiqueta = self.etiqueta
        self.etiqueta = new_while
        last_temp = self.procesar_operacion(sentenciaWhile.condicion,ts)
        new_temp = self.generarTemporal()
        new_cuadruplo2 =Cuadruplo("=","!",last_temp,new_temp)
        self.cuadruplos.add(new_cuadruplo2)
        self.etiquetas[self.etiqueta].append(new_cuadruplo2)
        new_cuadruplo2 =Cuadruplo("if",new_temp,"goto",new_etiqueta)
        self.cuadruplos.add(new_cuadruplo2)
        self.etiquetas[self.etiqueta].append(new_cuadruplo2)
        self.procesar_sentencias(sentenciaWhile.sentencias,ts)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        self.etiquetas[new_etiqueta] = []
        self.etiqueta = new_etiqueta

    def procesar_doWhile(self,sentencia, ts):
        new_do = self.generarDO()
        new_end = self.generarEND()
        new_while = self.generarWHILE()
        #generamos cuadruplo goto do
        new_cuadruplo = Cuadruplo("goto",new_do,"","")
        #lo agregamos a nuestra lista de cuadruplos
        self.cuadruplos.add(new_cuadruplo)
        #lo agregamos el cuadruplo a su etiqueta
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        #procedemos a crear la etiqueta do en nuestra lista de etiquetas para cuadruplos
        self.etiquetas[new_do] = []
        #guardamos el valor de etiqueta
        old_etiqueta = self.etiqueta
        #le asignamos el valor de do a la etiqueta globa
        self.etiqueta = new_do
        #ejecutamos todas las sentencias
        self.procesar_sentencias(sentencia.sentencias,ts)
        #creamos un cuadruplo para goto while
        new_cuadruplo = Cuadruplo("goto",new_while,"","")
        #lo agregamos a nuestra lista de cuadruplos
        self.cuadruplos.add(new_cuadruplo)
        #lo agregamos el cuadruplo a su etiqueta
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        #procedemos a crear la etiqueta while en nuestra lista de etiquetas para cuadruplos
        self.etiquetas[new_while] = []
        #cambiamos de etiqueta a while
        self.etiqueta = new_while
        #hacemos las operaciones 
        last_temp = self.procesar_operacion(sentencia.condicion,ts)
        #creamos un temporal
        new_temp = self.generarTemporal()
        #negamos el ultimo temporal retornado por la operacion
        new_cuadruplo2 =Cuadruplo("=","!",last_temp,new_temp)
        #lo agregamos a nuestros cuadruplos
        self.cuadruplos.add(new_cuadruplo2)
        #tambien lo agregamos a nuestra lista de etiquetas
        self.etiquetas[self.etiqueta].append(new_cuadruplo2)
        #creamos el if para salir del ciclo
        new_cuadruplo2 =Cuadruplo("if",new_temp,"goto",new_end)
        #lo agregamos a nuestros cuadruplos
        self.cuadruplos.add(new_cuadruplo2)
        #tambien lo agregamos a nuestra lista de etiquetas
        self.etiquetas[self.etiqueta].append(new_cuadruplo2)
        #ahora creamos el goto para regresar a do
        new_cuadruplo = Cuadruplo("goto",new_do,"","")
        #lo agregamos el cuadruplo a su etiqueta
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        self.etiqueta = new_end
        #procedemos a crear la etiqueta end en nuestra lista de etiquetas para cuadruplos
        self.etiquetas[new_end] = []
    
    def procesar_for(self,sentencia,ts):
        'aun no, ta muy feo xd'

    def procesar_llamada(self, sentencia, ts):
        #comparamos si estamos en la misma funcion
        if sentencia.id != self.ambito_ejecucion:
            #comprobamos si tiene parametros 
            self.ambito_ejecucion = sentencia.id
            if sentencia.params:
                primero = True
                for parametro in sentencia.params:
                    if primero:
                        new_cuadruplo = Cuadruplo("=","0","","$sp")
                        self.cuadruplos.add(new_cuadruplo)
                        self.etiquetas[self.etiqueta].append(new_cuadruplo)
                        primero = False
                    else:
                        new_cuadruplo = Cuadruplo("+","$sp","1","$sp")
                        self.cuadruplos.add(new_cuadruplo)
                        self.etiquetas[self.etiqueta].append(new_cuadruplo)

                    last_temp = self.procesar_operacion(parametro,ts)
                    new_cuadruplo =Cuadruplo("=",last_temp,"","$s0[$sp]")
                    self.cuadruplos.add(new_cuadruplo)
                    self.etiquetas[self.etiqueta].append(new_cuadruplo)
                    
            #comentario random
            old_etiqueta = self.etiqueta
            self.etiqueta = sentencia.id
            new_etiqueta = self.generarEtiqueta()
            self.etiquetas[new_etiqueta] = []
            self.etiqueta = old_etiqueta
            self.last_etiqueta = new_etiqueta
            new_cuadruplo = Cuadruplo("goto",new_etiqueta,"","")
            self.cuadruplos.add(new_cuadruplo)
            
            self.etiquetas[self.etiqueta].append(new_cuadruplo)  
            self.etiqueta = new_etiqueta
            #otro comentario random
            local = TablaSimbolos()
            local.setPadre(ts.getPadre())

            if sentencia.id in self.funciones:
                sentencias = self.funciones[sentencia.id]["sentencias"]
                params = self.funciones[sentencia.id]["params"]
                if params!=None and sentencia.params!=None:
                    #comprobamos si tienen el mismo numero de valores en sus parametros
                    if len(params) == len(sentencia.params):
                        #regresamos el apuntador hacia la primera posicion en la pila
                        new_cuadruplo = Cuadruplo("-", "$sp",str(len(params)-1),"$sp")
                        self.cuadruplos.add(new_cuadruplo)
                        self.etiquetas[self.etiqueta].append(new_cuadruplo)
                        #ahora asignamos los valores a una tabla local
                        contar_aux = 1
                        for param in params:
                            temp = self.generarTemporal()
                            new_simbol = Simbolo(param, temp, 0, 0)
                            local.add(new_simbol)
                            new_cuadruplo = Cuadruplo("=", "$s0[$sp]","",temp)
                            self.cuadruplos.add(new_cuadruplo)
                            self.etiquetas[self.etiqueta].append(new_cuadruplo)

                            if contar_aux == len(params):
                                ''
                            else:
                                new_cuadruplo = Cuadruplo("+", "$sp","1","$sp")
                                self.cuadruplos.add(new_cuadruplo)
                                self.etiquetas[self.etiqueta].append(new_cuadruplo)

                            contar_aux+=1
                self.procesar_sentencias(sentencias,local)
                #etiqueta para salir
                new_etiqueta = self.generarEND()
                self.etiquetas[new_etiqueta] = []
                new_cuadruplo = Cuadruplo("goto",new_etiqueta,"","")
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)  
                self.etiqueta = new_etiqueta

            else:
                'aqui deberiamos eliminar la etiqueta'
                del self.etiquetas[self.etiqueta]
                self.etiqueta = old_etiqueta
        else:
            'some action'
            print(">>AQUI DEBERIA ESTA EN EL MISMO AMBITO DE EJECUCION")
            print("{0},{1}".format(self.ambito_ejecucion,self.last_etiqueta))
            
            if sentencia.params:
                primero = True
                for parametro in sentencia.params:
                    if primero:
                        new_cuadruplo = Cuadruplo("=","0","","$sp")
                        self.cuadruplos.add(new_cuadruplo)
                        self.etiquetas[self.etiqueta].append(new_cuadruplo)
                        primero = False
                    else:
                        new_cuadruplo = Cuadruplo("+","$sp","1","$sp")
                        self.cuadruplos.add(new_cuadruplo)
                        self.etiquetas[self.etiqueta].append(new_cuadruplo)

                    last_temp = self.procesar_operacion(parametro,ts)
                    new_cuadruplo =Cuadruplo("=",last_temp,"","$s0[$sp]")
                    self.cuadruplos.add(new_cuadruplo)
                    self.etiquetas[self.etiqueta].append(new_cuadruplo)

            new_cuadruplo = Cuadruplo("goto",self.last_etiqueta,"","")
            self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)

    def procesar_switch(self, sentencia, ts):
        new_etiqueta = self.generarSWITCH()
        new_cuadruplo = Cuadruplo("goto",new_etiqueta, "","")
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        old_etiqueta = self.etiqueta
        self.etiqueta = new_etiqueta
        self.etiquetas[new_etiqueta] = []
        casos = []
        keys_casos = []
        default = None
        new_default= ""
        for caso in sentencia.casos:
            if caso.operacion:
                new_case = self.generarCASE()
                self.etiquetas[new_case] = []
                casos.append(caso)
                keys_casos.append(new_case)
            else:
                new_default = self.generarDEFAULT()
                self.etiquetas[new_default] = []
                default = caso
        #generar end para salir del ciclo
        new_end = self.generarEtiqueta()

        #primero, tenemos que tener la condicion
        last_temp = self.procesar_operacion(sentencia.condicion,ts)
        #area para traducir todos los casos
        actual_temp = self.generarTemporal()
        index = 0
        if casos:
            for caso in casos:
                op = self.procesar_operacion(caso.operacion,ts)
                new_cuadruplo = Cuadruplo("==",last_temp,op,actual_temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
                new_cuadruplo = Cuadruplo("if",actual_temp,"goto",keys_casos[index])
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
                index+=1

        if default:
            new_cuadruplo = Cuadruplo("goto",new_default, "","")
            self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)
        else:
            self.etiquetas[new_end] =[]
            new_cuadruplo = Cuadruplo("goto",new_end, "","")
            self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)

        actual = "" 
        index = 0
        if casos:
            for caso in casos:
                self.etiqueta = keys_casos[index]
                self.procesar_sentencias(caso.sentencias,ts)   
                if index + 1 < len(casos):
                    new_cuadruplo = Cuadruplo("goto",keys_casos[index+1], "","")
                    self.cuadruplos.add(new_cuadruplo)
                    self.etiquetas[self.etiqueta].append(new_cuadruplo)
            
                index+=1
     
        if default:
            new_cuadruplo = Cuadruplo("goto",new_default, "","")
            self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)
            #agregamos las acciones al default
            self.etiqueta = new_default
            self.procesar_sentencias(default.sentencias, ts)

        
        self.etiquetas[new_end] =[]
        new_cuadruplo = Cuadruplo("goto",new_end, "","")
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        #mandamos como etiqueta el fin 
        self.etiqueta = new_end
        


        






    def procesar_sentencias(self,sentencias, ts):
        local = TablaSimbolos()
        local.setPadre(ts)
        for sentencia in sentencias:
            if isinstance(sentencia,Declaraciones): self.procesar_declaraciones(sentencia,local)
            elif isinstance(sentencia,AsignacionSimple): self.procesar_asignacionSimple(sentencia,local)
            elif isinstance(sentencia,AsignacionCompuesta): self.procesar_asignacionCompuesta(sentencia,local)
            elif isinstance(sentencia,If):  self.procesar_if(sentencia,local)
            elif isinstance(sentencia,While): self.procesar_while(sentencia,local)
            elif isinstance(sentencia,DoWhile): self.procesar_doWhile(sentencia,local)
            elif isinstance(sentencia, Llamada): self.procesar_llamada(sentencia,local)
            elif isinstance(sentencia, Switch): self.procesar_switch(sentencia,local)
        


        

    def procesar_operacion(self, operacion, ts):
        if isinstance(operacion,OperacionNumero): return self.procesar_valor(operacion, ts)
        elif isinstance(operacion, OperacionCadena): return self.procesar_valor(operacion, ts)
        elif isinstance(operacion, OperacionCaracter): return self.procesar_valor(operacion, ts)
        elif isinstance(operacion, OperacionVariable): return self.procesar_valor(operacion, ts)
        elif isinstance(operacion, OperacionBinaria): return self.procesar_operacinBinaria(operacion,ts)
        elif isinstance(operacion, OperacionUnaria): return self.procesar_operacionUnaria(operacion,ts)

    def procesar_operacinBinaria(self,operacion,ts):
        
        op1 = self.procesar_operacion(operacion.operadorIzq,ts) #aqui dara un valor si es numero o un temporal 
        op2 = self.procesar_operacion(operacion.operadorDer,ts) #aqui dara un valor si es numero o un temporal 
        operador = operacion.operacion
        temp = self.generarTemporal()
        new_cuadruplo = Cuadruplo(operador,op1, op2, temp)
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        return temp
    
    def procesar_operacionUnaria(self,operacion,ts):
        op1 = self.procesar_operacion(operacion.operadorIzq,ts)
        operador = operacion.operacion
        temp = self.generarTemporal()
        new_cuadruplo = Cuadruplo(operador,op1, "", temp)
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        return temp

    def procesar_valor(self, expresion, ts):
        if isinstance(expresion,OperacionVariable): 
            if ts.existePadre(expresion.id,ts):
                val = ts.getValor(expresion.id, ts)
                temp = self.generarTemporal()
                new_cuadruplo = Cuadruplo("=",val.temporal,"",temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
                return temp
        else:
            return expresion.val
        

    def generarTemporal(self):
        #generamos un nuevo temporal del tipo $tn
        salida = "$t{0}".format(self.index_temporal)
        #aumentamos su contador para que no existan mismos temporales
        self.index_temporal += 1
        return salida

    def generarIF(self):
        #generamos una nueva etiqueta para los if
        salida = "if{0}".format(self.index_if)
        #aumentamos su contador para que no existan mismos temporales
        self.index_if += 1
        return salida
        
    def generarWHILE(self):
        #generamos una nueva etiqueta para los if
        salida = "while{0}".format(self.index_while)
        #aumentamos su contador para que no existan mismos temporales
        self.index_while += 1
        return salida

    def generarSWITCH(self):
        #generamos una nueva etiqueta para los if
        salida = "switch{0}".format(self.index_switch)
        #aumentamos su contador para que no existan mismos temporales
        self.index_switch += 1
        return salida

    def generarCASE(self):
        #generamos una nueva etiqueta para los if
        salida = "case{0}".format(self.index_case)
        #aumentamos su contador para que no existan mismos temporales
        self.index_case += 1
        return salida

    def generarDEFAULT(self):
        #generamos una nueva etiqueta para los if
        salida = "default{0}".format(self.index_default)
        #aumentamos su contador para que no existan mismos temporales
        self.index_default += 1
        return salida

    def generarDO(self):
        #generamos una nueva etiqueta para los if
        salida = "do{0}".format(self.index_do)
        #aumentamos su contador para que no existan mismos temporales
        self.index_do += 1
        return salida

    def generarEND(self):
        #generamos una nueva etiqueta para los if
        salida = "end{0}".format(self.index_end)
        #aumentamos su contador para que no existan mismos temporales
        self.index_end += 1
        return salida

    def generarEtiqueta(self):
        #generamos una nueva etiqueta
        salida = "{0}{1}".format(self.ambito_ejecucion,self.index_etiquetas)
        #aumentamos su contador para que no existan mismos temporales
        self.index_etiquetas += 1
        return salida

    def generarHeap(self):
        #generamos una nueva etiqueta
        salida = "$s1[{0}]".format(self.index_heap)
        #aumentamos su contador para que no existan mismos temporales
        self.index_heap += 1
        return salida