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
        self.index_if = 0
        self.index_etiquetas = 0
        self.index_while=0
        self.index_end = 0


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
                    self.C3D.addItem(" goto {0};".format(cuadruplo.result))
                    print(" goto {0};".format(cuadruplo.result))
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
        for instruccion in instrucciones:
            if isinstance(instruccion, Declaraciones): self.recolectar_declaraciones(instruccion)
            elif isinstance(instruccion, Main): self.recolectar_main(instruccion)
            elif isinstance(instruccion, Metodo): self.recolectar_metodo(instruccion)
            elif isinstance(instruccion, Funcion): self.recolectar_funcion(instruccion)


    def recolectar_main(self, instruccion):
        if not "main" in self.funciones:
            self.funciones["main"] = instruccion.sentencias

    def recolectar_metodo(self, instruccion):
        if not instruccion.id in self.funciones:
            self.funciones[instruccion.id] = instruccion.sentencias

    def recolectar_funcion(self, instruccion):
        if not instruccion.id in self.funciones:
            self.funciones[instruccion.id] = instruccion.sentencias

    def recolectar_declaraciones(self,instruccion):
        for instru in instruccion.declaraciones:
            self.recolectar_declaracion(instru)

    def recolectar_declaracion(self, instruccion):
        id = instruccion.id
        if not self.ts.existe(id):
            if instruccion.valor:
                last_temp = self.procesar_operacion(instruccion.valor,self.ts)
                temp = self.generarTemporal()
                new_simbol = Simbolo(id, temp, instruccion.line, instruccion.column)
                self.ts.add(new_simbol)
                new_cuadruplo = Cuadruplo("=", last_temp,"",temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            else:
                temp = self.generarTemporal()
                new_simbol = Simbolo(id, temp, instruccion.line, instruccion.column)
                self.ts.add(new_simbol)
                new_cuadruplo = Cuadruplo("=", "0","",temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
                
        
    def procesar(self):
        if "main" in self.funciones:
            self.procesar_main(self.funciones["main"], self.ts)
    
    def procesar_main(self, sentencias, ts):
        self.etiqueta = "main"
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
            temp = ts.getValor(id, ts).temporal
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
        new_cuadruplo = Cuadruplo("goto", "","",new_etiqueta)
        #self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        self.etiqueta = old_etiqueta
        #ciclo para elseif
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
            new_cuadruplo = Cuadruplo("goto", "","",new_etiqueta)
            #self.cuadruplos.add(new_cuadruplo)
            self.etiquetas[self.etiqueta].append(new_cuadruplo)
            self.etiqueta = old_etiqueta
        #else
        self.etiqueta = old_etiqueta
        self.procesar_sentencias(s_else.sentencias,ts)
        #creamos una nueva etiqueta que nos diriga hacia lo que traia el main
        new_cuadruplo = Cuadruplo("goto", "","",new_etiqueta)
        self.cuadruplos.add(new_cuadruplo)
        self.etiquetas[self.etiqueta].append(new_cuadruplo)
        self.etiquetas[new_etiqueta] = []
        self.etiqueta = new_etiqueta

    def procesar_while(self,sentenciaWhile, ts):
        new_etiqueta = self.generarEND()
        new_while = self.generarWHILE()
        new_cuadruplo = Cuadruplo("goto", "","",new_while)
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



    def procesar_sentencias(self,sentencias, ts):
        local = TablaSimbolos()
        local.setPadre(ts)
        for sentencia in sentencias:
            if isinstance(sentencia,Declaraciones): self.procesar_declaraciones(sentencia,local)
            elif isinstance(sentencia,AsignacionSimple): self.procesar_asignacionSimple(sentencia,local)
            elif isinstance(sentencia,AsignacionCompuesta): self.procesar_asignacionCompuesta(sentencia,local)
            elif isinstance(sentencia,If):  self.procesar_if(sentencia,local)
            elif isinstance(sentencia,While): self.procesar_while(sentencia,local)
        


        

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
                return val.temporal
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

    def generarEND(self):
        #generamos una nueva etiqueta para los if
        salida = "end{0}".format(self.index_end)
        #aumentamos su contador para que no existan mismos temporales
        self.index_end += 1
        return salida

    def generarEtiqueta(self):
        #generamos una nueva etiqueta
        salida = "{0}{1}".format(self.etiqueta,self.index_etiquetas)
        #aumentamos su contador para que no existan mismos temporales
        self.index_etiquetas += 1
        return salida