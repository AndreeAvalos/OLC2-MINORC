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


    def run(self):
        self.recolectar(self.ast)
        self.procesar()
        self.imprimirCuadruplos()
        self.imprimir3D()

    def imprimir3D(self):
        for etiqueta in self.etiquetas:
            self.C3D.addItem(etiqueta+":")
            for cuadruplo in self.etiquetas[etiqueta]:
                if cuadruplo.op != "=":
                    self.C3D.addItem(" {0}={1} {2} {3};".format(cuadruplo.result,cuadruplo.arg1, cuadruplo.op, cuadruplo.arg2))
                else:
                    self.C3D.addItem(" {0}={1};".format(cuadruplo.result,cuadruplo.arg1))

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
        local = TablaSimbolos()
        local.setPadre(ts)
        for sentencia in sentencias:
            if isinstance(sentencia,Declaraciones): self.procesar_declaraciones(sentencia,local)
            elif isinstance(sentencia,AsignacionSimple): self.procesar_asignacionSimple(sentencia,local)
            elif isinstance(sentencia,AsignacionCompuesta): self.procesar_asignacionCompuesta(sentencia,local)

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
                new_cuadruplo = Cuadruplo("-", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '/=':
                new_cuadruplo = Cuadruplo("-", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '%=':
                new_cuadruplo = Cuadruplo("-", temp,last_temp,temp)
                self.cuadruplos.add(new_cuadruplo)
                self.etiquetas[self.etiqueta].append(new_cuadruplo)
            elif operacion == '-=':
                new_cuadruplo = Cuadruplo("-", temp,last_temp,temp)
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