import sys
sys.path.append('./augus')
from InstruccionA import *
from Operacion import *
from TablaSimbolosA import Simbolo, TablaSimbolosA, Tipo_Salida 
from Recolectar import TokenError, Recolectar 
import threading
import time
import re 
from ArbolCaracteres import ArbolCaracteres
from Arreglo import Arreglo
import sys
from PyQt5 import QtWidgets,QtCore
class Ejecutor(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.instrucciones = args[0]
        self.ts = args[1]
        self.ambito ="global"
        self.lst_errores = args[2]
        self.entrada = args[3]
        self.leido = False
        #self.area = args[4]
        self.consola = args[4]
        self.last = ""
        self.encontro_if = False
        sys.setrecursionlimit(5000)
        self.step = True
        self.continuar = False
        self.detener = False
        self.procedimiento = False
        self.funcion = False
        self.control = False 
        self.GTS = args[5]


    def run(self):
        #temp =  self.area.currentLineColor
        try:      
            self.procesar()
            #self.join()
        except:
            print("ERROR DE EJECUCION")
        finally:
            #self.ts.graficarSimbolos()
            #self.graficarErrores()
            self.fullGTS()
            self.stop()
            self._stop = True
            return
    

    def setParams(self,in_,state):
        self.entrada= in_
        self.leido= state

    def agregarError(self,descripcion,line,column):
        new_error = TokenError("Semantico",descripcion,line,column)
        self.lst_errores.append(new_error)

    def graficarErrores(self):
        try:
            file = open("ESemanticos.dot", "w")
            file.write("digraph tablaErrores{\n")
            file.write("graph [ratio=fill];node [label=\"\\N\", fontsize=15, shape=plaintext];\n")
            file.write("graph [bb=\"0,0,352,154\"];\n")
            file.write("arset [label=<")
            file.write("<TABLE ALIGN=\"LEFT\">\n")
            file.write("<TR><TD>TIPO</TD><TD>DESCRIPCION</TD><TD>LINEA</TD><TD>COLUMNA</TD></TR>\n")
            for token in self.lst_errores:
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
            self.ts.cmd("dot -Tpng ESemanticos.dot -o ESemanticos.png")


    def procesar(self):
        encontro = False
        exit = False
        last_instruccion =False
        self.encontro_if = False
        continuar = False
        for instruccion in self.instrucciones:
            if isinstance(instruccion, Main): encontro = True
            if instruccion.id == self.last: 
                last_instruccion = True
                continue
            if encontro:
                if isinstance(instruccion,Main): 
                    exit = self.procesar_main(instruccion)
                    if exit == Tipo_Salida.EXIT:
                        return exit
                        
                if self.encontro_if == True:
                    if isinstance(instruccion, Etiqueta) and last_instruccion ==True:
                        exit = self.procesar_etiqueta(instruccion)
                elif isinstance(instruccion, Etiqueta):
                    exit = self.procesar_etiqueta(instruccion)

                if exit == Tipo_Salida.EXIT:
                    return exit

    def procesar_main(self,main):
        if not isinstance(main.sentencias,Vacio):
            self.ambito = "main"
            exit = False
            self.control = True
            self.funcion = False
            self.procedimiento = False
            for sentencia in main.sentencias:
                exit = Tipo_Salida.SEGUIR
                
                if self.detener:
                    return
                if isinstance(sentencia, Asignacion): self.procesar_asignacion(sentencia)
                elif isinstance(sentencia, Referencia): self.procesar_referencia(sentencia)
                elif isinstance(sentencia, Goto): exit = self.procesar_goto(sentencia)
                elif isinstance(sentencia, Exit): return Tipo_Salida.EXIT
                elif isinstance(sentencia, UnSet): self.procesar_unset(sentencia)
                elif isinstance(sentencia, If_): exit = self.procesar_if(sentencia)
                elif isinstance(sentencia, Print_): self.procesar_print(sentencia)
                elif isinstance(sentencia, Read): self.procesar_read(sentencia)
                elif isinstance(sentencia, AsignacionArreglo): self.procesar_arreglo(sentencia)
                elif isinstance(sentencia, DeclararArreglo): self.procesar_declaracionArreglo(sentencia)
                if exit == Tipo_Salida.EXIT:
                    return exit
                if exit == Tipo_Salida.DESCARTAR:
                    return exit

                
        return Tipo_Salida.SEGUIR

    def procesar_etiqueta(self, etiqueta):
        if not isinstance(etiqueta.sentencias,Vacio):
            self.ambito = etiqueta.id
            exit = False
            self.control = True
            self.funcion = False
            self.procedimiento = False

            for sentencia in etiqueta.sentencias:
                if self.detener:
                    return
                exit = Tipo_Salida.SEGUIR
                if isinstance(sentencia, Asignacion): self.procesar_asignacion(sentencia)
                elif isinstance(sentencia, Referencia): self.procesar_referencia(sentencia)
                elif isinstance(sentencia, Goto): exit = self.procesar_goto(sentencia)
                elif isinstance(sentencia, Exit): return Tipo_Salida.EXIT
                elif isinstance(sentencia, UnSet): self.procesar_unset(sentencia)
                elif isinstance(sentencia, If_): exit = self.procesar_if(sentencia)
                elif isinstance(sentencia, Print_): self.procesar_print(sentencia)
                elif isinstance(sentencia, Read): self.procesar_read(sentencia)
                elif isinstance(sentencia, AsignacionArreglo): self.procesar_arreglo(sentencia)
                elif isinstance(sentencia, DeclararArreglo): self.procesar_declaracionArreglo(sentencia)
                
                if exit == Tipo_Salida.EXIT:
                    return exit
                if exit == Tipo_Salida.DESCARTAR:
                    return exit

        return Tipo_Salida.SEGUIR
    
    def procesar_goto(self,sentencia):
        if self.ts.existe(sentencia.id):
            simbol = self.ts.get(sentencia.id)
            if simbol.tipo == Tipo_Simbolo.ETIQUETA:
                ambito = self.ambito
                self.encontro_if = True
                self.last = sentencia.id
                self.actualizarEtiqueta(sentencia.id)
                existe = self.procesar_etiqueta(simbol)
                self.ambito = ambito
                return existe
            else:
                self.agregarError("{0} no es una etiqueta".format(sentencia.id),sentencia.line, sentencia.column)
        else:
            self.agregarError("{0} no esta declarado".format(sentencia.id),sentencia.line,sentencia.column)

        return Tipo_Salida.EXIT
    
    def procesar_unset(self, sentencia):
        try:
            if self.ts.existe(sentencia.id):
                self.ts.delete(sentencia.id)
            else:
                self.agregarError("{0} no esta declarado".format(sentencia.id),sentencia.line,sentencia.column)     
        except:
            self.agregarError("Error al eliminar",sentencia.line,sentencia.column)

    def procesar_if(self, sentencia):
        operacion = sentencia.operacion
        if isinstance(operacion,OperacionRelacional) or isinstance(operacion,OperacionLogica) or isinstance(operacion, OperacionNumero) or isinstance(operacion,OperacionVariable) or isinstance(operacion,OperacionCopiaVariable):
            result = self.procesar_operacion(operacion)
            operando = False
            
            if result == 1:
                operando = True
            elif result == 0:
                operando = False
            else:
                self.agregarError("{0} valor invalido".format(result))
                return Tipo_Salida.SEGUIR
            if operando:
                self.encontro_if = True
                self.last = sentencia.goto.id
                salida = self.procesar_goto(sentencia.goto)
                if salida == Tipo_Salida.EXIT:
                    return Tipo_Salida.EXIT
                else:
                    return Tipo_Salida.DESCARTAR
        elif isinstance(operacion, OperacionUnaria):
            result = self.procesar_operacion(operacion)
            if sentencia.operacion.operacion == OPERACION_LOGICA.NOT:
                operando = False
                if result == 1:
                    operando = True
                elif result == 0:
                    operando = False
                else:
                    self.agregarError("{0} valor invalido".format(result))
                    return Tipo_Salida.SEGUIR
                if operando:
                    self.encontro_if = True
                    self.last = sentencia.goto.id
                    salida = self.procesar_goto(sentencia.goto)
                    if salida == Tipo_Salida.EXIT:
                        return Tipo_Salida.EXIT
                    else:
                        return Tipo_Salida.DESCARTAR
        else:
            self.agregarError("Operacion no valida",sentencia.line,sentencia.column)
        return Tipo_Salida.SEGUIR

    def procesar_print(self, sentencia):
        if isinstance(sentencia.val, OperacionCopiaVariable):
            result = self.procesar_valor(sentencia.val)
        
            if isinstance(result, ArbolCaracteres):
                self.consola.insertHtml(str(result.getText()))
                #self.consola.append(str(result.getText()))
            elif isinstance(result, Arreglo):
                self.agregarError("No se puede imprimir un arreglo", sentencia.line, sentencia.column)
            elif result!=None:
                self.consola.insertHtml(str(result))
        elif isinstance(sentencia.val, OperacionArreglo):
            result = self.procesar_opeacionArreglo(sentencia.val)
            if isinstance(result, ArbolCaracteres):
                self.consola.insertHtml(str(result.getText()))
            elif isinstance(result, Arreglo):
                self.agregarError("No se puede imprimir un arreglo", sentencia.line, sentencia.column)
            elif result!=None:
                self.consola.insertHtml(str(result))
        elif isinstance(sentencia.val, OperacionCadena):
            result = self.procesar_cadena(sentencia.val)
            if isinstance(result, ArbolCaracteres):
                if str(result.getText())=="\\n":
                    self.consola.append("")
                else:
                    self.consola.insertHtml(str(result.getText()))
        time.sleep(0.1)
        return Tipo_Salida.SEGUIR
    
    def procesar_read(self,sentencia2):
        sentencia = sentencia2.sentencia
        self.consola.append("")
        new_simbol = Simbolo(sentencia.id, None, None, sentencia.tipo,self.ambito, sentencia.etiqueta,sentencia.line,sentencia.column)
        self.ts.add(new_simbol)
        id = sentencia.id
        entero = r'-?[0-9]+'
        decimal = r'-?[0-9]+\.[0-9]+'
        string = r'.*'

        if self.ts.existe(id):
            contador = 0 #contador para contar los segundos de tiempo de lida maxima
            self.leido = False
            while contador <100:
                time.sleep(0.4)
                if self.leido:
                    if re.match(entero,self.entrada):
                        self.ts.set(id,int(self.entrada))
                    elif re.match(decimal,self.entrada):
                        self.ts.set(id,float(self.entrada))
                    elif re.match(string,self.entrada):
                        arbol = ArbolCaracteres(self.entrada)
                        self.ts.set(id,arbol)
                    else:
                        self.agregarError("{0} dato no aceptado".format(self.entrada),sentencia.line, sentencia.column)
                    time.sleep(0.5)
                    return Tipo_Salida.SEGUIR
                contador = contador + 1
            self.agregarError("Tiempo de ejecucion agotado",sentencia.line,sentencia.column)
        return Tipo_Salida.SEGUIR

    def procesar_asignacion(self, sentencia):
        if sentencia.tipo != Tipo_Simbolo.INVALIDO:
            self.activarBanderas(sentencia.tipo)
            result = self.procesar_operacion(sentencia.valor)
            if result != None:
                if not self.ts.existe(sentencia.id):
                    new_simbol = Simbolo(sentencia.id, None, result, sentencia.tipo,self.ambito, sentencia.etiqueta,sentencia.line,sentencia.column)
                    self.ts.add(new_simbol)
                else:
                    old_simbol = self.ts.get(sentencia.id)
                    if isinstance(old_simbol.valor.get(),Arreglo):
                        self.agregarError("{0} es un arreglo, no puede cambiar de tipo".format(sentencia.id),sentencia.line,sentencia.column)
                    else:
                        new_simbol = Simbolo(sentencia.id, None, result, sentencia.tipo,old_simbol.ambiente, sentencia.etiqueta,old_simbol.line,old_simbol.column)
                        self.ts.actualizar(new_simbol)
        else:
            self.agregarError("La variable {0} invalida".format(sentencia.id),sentencia.line, sentencia.column)

    def procesar_declaracionArreglo(self, sentencia):
        if sentencia.tipo != Tipo_Simbolo.INVALIDO:
            self.activarBanderas(sentencia.tipo)
            if not self.ts.existe(sentencia.id):
                new_simbol = Simbolo(sentencia.id, None, Arreglo(), sentencia.tipo,self.ambito, sentencia.etiqueta,sentencia.line,sentencia.column)
                self.ts.add(new_simbol)
            else:
                self.agregarError("{0} no puede cambiar su tipo a arreglo".format(sentencia.id),sentencia.line,sentencia.column)
        else:
            self.agregarError("La variable {0} invalida".format(sentencia.id),sentencia.line, sentencia.column)       
    
    def procesar_arreglo(self,sentencia):
        if sentencia.tipo != Tipo_Simbolo.INVALIDO:
            result = self.procesar_operacion(sentencia.valor)
            numerico = True
            if result!=None:
                #hacemos una lista de indices para poder ingresarlos a nuestro diccionario 
                direcciones = []
                for dimension in sentencia.dimensiones:
                    indice = self.procesar_operacion(dimension)
                    if indice==None:
                        self.agregarError("indice no valido",dimension.line,dimension.column)
                        return
                    texto = indice
                    if isinstance(indice,ArbolCaracteres):
                        texto = indice.getText()
                        numerico=False
                    
                    direcciones.append(texto)
                  #terminamos de parsear los valores a una lista  
                if not self.ts.existe(sentencia.id):
                    #Si no existe es porque no se ha declarado la variable como arreglo, por ende no se puede asignar el valor 
                    self.agregarError("{0} no es un arreglo".format(sentencia.id),sentencia.line, sentencia.column)
                else:
                    #Aqui debemos comprobar que el valor de la variable sea un arreglo, de lo contrario seria un error
                    #dado que no puede cambiar de un tipo primitivo a un arreglo segun las indicaciones del auxiliar
                    simbolo = self.ts.get(sentencia.id)
                    #Comparamos si el valor del simbolo es un valor de arreglo
                    if isinstance(simbolo.valor.get(), Arreglo):
                        #aqui ya debemos hacer las comparaciones con si existe los indices
                        # primero debemos comprobar si existen los los indices
                        arreglo_auxiliar = simbolo.valor.get()
                        existen_indices =  arreglo_auxiliar.exist(direcciones)
                        #si no existe entonces comprobamos que si el ultimo no sea un arbol de caracteres
                        if not existen_indices:
                            isarbol = arreglo_auxiliar.isThree(direcciones)                    
                            if not isarbol:
                                arreglo_auxiliar.add(direcciones, result)
                                simbolo.valor.set(arreglo_auxiliar)
                                if numerico:
                                    simbolo.etiqueta = Tipo_Etiqueta.ARREGLONUMERICO
                                else:
                                    simbolo.etiqueta = Tipo_Etiqueta.STRUCT
                                self.ts.add(simbolo)
                            else:
                                #aqui debemos cambiar los caracteres de la cadena
                                resultado = arreglo_auxiliar.setChars(direcciones, result.getText())
                                
                                if resultado == False:
                                    self.agregarError("index {0} no permitido".format(direcciones[len(direcciones)-1]),sentencia.line,sentencia.column)
                                return
                        else:
                            arreglo_auxiliar.setValue(direcciones,result)
                            simbolo.valor.set(arreglo_auxiliar)
                            if numerico:
                                simbolo.etiqueta = Tipo_Etiqueta.ARREGLONUMERICO
                            else:
                                simbolo.etiqueta = Tipo_Etiqueta.STRUCT
                            self.ts.add(simbolo)
                    else:
                            self.agregarError("{0} no es un arreglo".format(sentencia.id),sentencia.line, sentencia.column)


        else:
            self.agregarError("La variable {0} invalida".format(sentencia.id),sentencia.line, sentencia.column)

    def procesar_referencia(self, sentencia):
        if sentencia.tipo != Tipo_Simbolo.INVALIDO:
            self.activarBanderas(sentencia.tipo)
            result = self.procesar_valor(sentencia.valor)
            if result != None:
                if not self.ts.existe(sentencia.id):
                    new_simbol = Simbolo(sentencia.id, None, None, sentencia.tipo,self.ambito, sentencia.etiqueta,sentencia.line,sentencia.column)
                    self.ts.add(new_simbol)
                    self.ts.referenciar(sentencia.id, result.valor)
                else:
                    self.ts.referenciar(sentencia.id, result.valor)
        else:
            self.agregarError("La variable {0} invalida".format(sentencia.id),sentencia.line, sentencia.column)       


    def procesar_operacion(self,operacion):
        if isinstance(operacion,OperacionNumerica): return self.procesar_operacionNumerica(operacion)
        elif isinstance(operacion, OperacionNumero): return self.procesar_valor(operacion)
        elif isinstance(operacion, OperacionCadena): return self.procesar_cadena(operacion)
        elif isinstance(operacion, OperacionCopiaVariable): return self.procesar_valor(operacion)
        elif isinstance(operacion, OperacionLogica): return self.procesar_operacionLogica(operacion)
        elif isinstance(operacion, OperacionUnaria): return self.procesar_operacionUnaria(operacion)
        elif isinstance(operacion,OperacionRelacional): return self.procesar_operacionRelacional(operacion)
        elif isinstance(operacion, OperacionArreglo):   return self.procesar_opeacionArreglo(operacion)
        elif isinstance(operacion, OperacionCasteo): return self.procesar_casteo(operacion)
        elif isinstance(operacion, OperacionBit): return self.procesar_operacionBit(operacion)

    def procesar_operacionNumerica(self, operacion):
        try:
            
            if operacion.operacion == OPERACION_NUMERICA.SUMA: 
                op1 = self.procesar_valor(operacion.operadorIzq)
                op2 = self.procesar_valor(operacion.operadorDer)
                
                if isinstance(op1,ArbolCaracteres) and isinstance(op2,ArbolCaracteres):
                    return op1.getText() + op2.getText()        
                else:
                    return op1 + op2
                return self.procesar_valor(operacion.operadorIzq) + self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.RESTA: return self.procesar_valor(operacion.operadorIzq) - self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.MULTIPLICACION: return self.procesar_valor(operacion.operadorIzq) * self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.DIVISION: return self.procesar_valor(operacion.operadorIzq) / self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_NUMERICA.MODULAR: return self.procesar_valor(operacion.operadorIzq) % self.procesar_valor(operacion.operadorDer)
        except:
            self.agregarError("No es posible la operacion numerica",operacion.line,operacion.column)

    def procesar_operacionLogica(self, operacion):
        op1 = self.procesar_valor(operacion.operadorIzq)
        op2 = self.procesar_valor(operacion.operadorDer)
        izq = False
        der = False
        if op1 == 1: 
            izq = True
        elif op1 ==0:
            izq = False
        else:
            self.agregarError("{0} invalido para operacion logica".format(op1),operacion.line, operacion.column)
            return 0

        if op2 == 1: 
            der = True
        elif op2 == 0:
            der = False
        else:
            self.agregarError("{0} invalido para operacion logica".format(op2),operacion.line, operacion.column)
            return 0

        if operacion.operacion == OPERACION_LOGICA.AND: 
            return 1 if(izq and der) else 0
        elif operacion.operacion == OPERACION_LOGICA.OR: 
            return 1 if(izq or der) else 0
        elif operacion.operacion == OPERACION_LOGICA.XOR:
            op1 = izq
            op2 = der
            r_notand = not( op1 and op2)
            r_or =   op1 or op2
            r_xor = r_notand and r_or
            return 1 if(r_xor) else 0

    def procesar_operacionRelacional(self, operacion):
        try:
            op1 = self.procesar_valor(operacion.operadorIzq)
            op2 = self.procesar_valor(operacion.operadorDer)
            if isinstance(op1, ArbolCaracteres):op1 = op1.getText()
            if isinstance(op2, ArbolCaracteres):op2 = op2.getText()
            
            if operacion.operacion == OPERACION_RELACIONAL.IGUAL: return 1 if(op1 == op2) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.DIFERENTE: return 1 if(op1 != op2) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MAYORQUE: return 1 if(op1 >= op2) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MENORQUE: return 1 if(op1 <= op2) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MAYOR: return 1 if(op1 > op2) else 0
            elif operacion.operacion == OPERACION_RELACIONAL.MENOR: return 1 if(op1 < op2) else 0
        except:
            self.agregarError("No es posible la operacion relacional",operacion.line,operacion.column)

    def procesar_operacionBit(self,operacion):
        try:
            if operacion.operacion == OPERACION_BIT.AND: return self.procesar_valor(operacion.operadorIzq) & self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_BIT.OR: return self.procesar_valor(operacion.operadorIzq) | self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_BIT.XOR: return self.procesar_valor(operacion.operadorIzq) ^ self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_BIT.SHIFTIZQ: return self.procesar_valor(operacion.operadorIzq) << self.procesar_valor(operacion.operadorDer)
            elif operacion.operacion == OPERACION_BIT.SHIFTDER: return self.procesar_valor(operacion.operadorIzq) >> self.procesar_valor(operacion.operadorDer)
        except:
            self.agregarError("No es posible operar bit a bit",operacion.line,operacion.column)


    def procesar_operacionUnaria(self,operacion):
        op1 = self.procesar_valor(operacion.operadorIzq) 
        if operacion.operacion == OPERACION_BIT.NOT:
            if isinstance(op1, int):
                return ~op1
            else:
                self.agregarError("{0} no es un valor entero".format(op1),operacion.line, operacion.column)

        elif operacion.operacion == OPERACION_LOGICA.NOT:
            if op1==1:
                return 0
            elif op1 == 0:
                return 1
            else:
                self.agregarError("El Numero {0} no puede ser negado".format(op1),operacion.line, operacion.column)
                return 0
        elif operacion.operacion == OPERACION_NUMERICA.RESTA:
            if isinstance(op1, int) or isinstance(op1,float):
                return -1*op1
            else:
                self.agregarError("{0} no es un valor numerico".format(op1),operacion.line,operacion.column)
                return op1
        elif operacion.operacion == OPERACION_NUMERICA.ABSOLUTO:
            if isinstance(op1, int) or isinstance(op1,float):
                return abs(op1)
            else:
                self.agregarError("{0} no es un valor numerico".format(op1),operacion.line,operacion.column)
                return op1

    def procesar_opeacionArreglo(self,operacion):
        if self.ts.existe(operacion.id):
            simbolo = self.ts.get(operacion.id)
            arbol = simbolo.valor.get()
            if isinstance(arbol,Arreglo):
                direcciones = []
                for dimension in operacion.dimensiones:
                    indice = self.procesar_operacion(dimension)
                    if indice==None:
                        self.agregarError("indice no valido",dimension.line,dimension.column)
                        return
                    texto = indice
                    if isinstance(indice,ArbolCaracteres):
                        texto = indice.getText()
                        numerico=False
                    
                    direcciones.append(texto)
                if arbol.exist(direcciones):
                    ret = arbol.getValue(direcciones)
                    return arbol.getValue(direcciones)
                else:
                    if arbol.isThree(direcciones):
                        arbol2 = arbol.getValue(direcciones[0:len(direcciones)-1])
                        if arbol2.valid(direcciones[len(direcciones)-1]):
                            return arbol2.indexOf(direcciones[len(direcciones)-1])
                        else:
                            self.agregarError("Indice {0} inalcanzable".format(direcciones[len(direcciones)-1]),operacion.line, operacion.column)
                            return
                    else:
                        self.agregarError("{0} no es un valor numerico".format(direcciones[len(direcciones)-1]),operacion.line, operacion.column)
                        return


                    self.agregarError("Indices inexistentes",operacion.line,operacion.column)
            elif isinstance(arbol, ArbolCaracteres):
                direcciones = []
                for dimension in operacion.dimensiones:
                    indice = self.procesar_operacion(dimension)
                    if indice==None:
                        self.agregarError("indice no valido",dimension.line,dimension.column)
                        return
                    texto = indice
                    if isinstance(indice,ArbolCaracteres):
                        texto = indice.getText()
                        numerico=False
                    
                    direcciones.append(texto)
                if len(direcciones)==1:
                    if isinstance(direcciones[0],int):
                        if arbol.valid(direcciones[0]):
                            return arbol.indexOf(direcciones[0])
                        else:
                            self.agregarError("Indice {0} inalcanzable".format(direcciones[0]),operacion.line, operacion.column)
                    else:
                        self.agregarError("{0} no es un valor numerico".format(direcciones[0]),operacion.line, operacion.column)
                else:
                    self.agregarError("Indices fuera del rango de un stirng",operacion.line, operacion.column)
            else:
                self.agregarError("{0} no es tipo arreglo".format(operacion.id),operacion.line, operacion.column)
        else:
            self.agregarError("{0} no existe variable".format(operacion.id),operacion.line, operacion.column)
                    

    def procesar_valor(self,expresion):
        if isinstance(expresion,OperacionNumero):
            if isinstance(expresion.val,int): return int(expresion.val)
            elif isinstance(expresion.val, float): return float(expresion.val)
            else: 
                self.agregarError("No existe tipo",expresion.line,expresion.column)
                return None
        elif isinstance(expresion, OperacionVariable):
            if self.ts.existe(expresion.id):
                return self.ts.get(expresion.id)
            else:
                self.agregarError("No existe variable {0}".format(expresion.id),expresion.line,expresion.column)
                return None
        elif isinstance(expresion, OperacionCopiaVariable):
            if self.ts.existe(expresion.id):
                return self.ts.get(expresion.id).valor.get()
            else:
                self.agregarError("No existe variable {0}".format(expresion.id),expresion.line,expresion.column)
                return None
        elif isinstance(expresion, OperacionCadena):
            return self.procesar_cadena(expresion)
            
        return None

    def procesar_cadena(self, expresion):
        if isinstance(expresion, OperacionCadena):
            return ArbolCaracteres(expresion.val)
    
    def procesar_casteo(self, expresion):
        result = self.procesar_operacion(expresion.expresion)
        if result!=None:
            return self.castear(expresion.tipo, result)
        return None

    def castear(self, tipo, result):
        if tipo == "int":
            if isinstance(result, int):
                return result
            elif isinstance(result,float):
                return int(result)
            elif isinstance(result, ArbolCaracteres):
                return ord(result.indexOf(0))
            elif isinstance(result,Arreglo):
                return self.castear(tipo, result.firstElement())
        elif tipo == "float":
            if isinstance(result, int):
                return float(result)
            elif isinstance(result,float):
                return result
            elif isinstance(result, ArbolCaracteres):
                return float(ord(result.indexOf(0)))
            elif isinstance(result,Arreglo):
                return self.castear(tipo, result.firstElement())
        elif tipo == "char":
            if isinstance(result, int):
                if result>=0 and result<=255:
                    char = chr(result)
                elif result>255:
                    new_result = result%256
                    char = chr(new_result)
                return ArbolCaracteres(str(char))
            elif isinstance(result, float):
                return self.castear(tipo, int(result))
            elif isinstance(result,ArbolCaracteres):
                return self.castear(tipo,ord(result.indexOf(0)))
            elif isinstance(result,Arreglo):
                return self.castear(tipo, result.firstElement(result.diccionario))
            elif isinstance(result,dict):
                aux = Arreglo()
                return self.castear(tipo,aux.firstElement(result))
                    
    def actualizarEtiqueta(self,id):
        if self.procedimiento:
            self.ts.etiqueta(id,Tipo_Etiqueta.PROCEDIMIENTO)
            return
        else :
            self.ts.etiqueta(id,Tipo_Etiqueta.CONTROL)
            return
    
    def activarBanderas(self, tipo):
        if tipo == Tipo_Simbolo.PARAMETRO or tipo == Tipo_Simbolo.SIMULADOR:
            self.procedimiento = True
            self.control = False
        elif tipo == Tipo_Simbolo.RETORNO:
            self.control = False
            self.funcion = True
            self.ts.etiqueta(self.ambito,Tipo_Etiqueta.FUNCION)

    def fullGTS(self):
        datos = []
        for id in self.ts.simbolos:
            if isinstance(self.ts.simbolos[id].valor.get(),ArbolCaracteres):
                datos.append((self.ts.simbolos[id].id,str(self.ts.simbolos[id].valor.get().getText())))
            elif isinstance(self.ts.simbolos[id].valor.get(),Arreglo):
                datos.append((self.ts.simbolos[id].id,"Arreglo"))
            else:
                datos.append((self.ts.simbolos[id].id,str(self.ts.simbolos[id].valor.get())))
        for i in range(self.GTS.rowCount()):
            self.GTS.removeRow(i)
        self.GTS.clearContents()

        fila = 0
        for registro in datos:
            columna = 0
            self.GTS.insertRow(fila)
            for item in registro:
                celda = QtWidgets.QTableWidgetItem(item)
                self.GTS.setItem(fila,columna,celda)
                columna+=1
            fila+=1

    def stop(self):
        self.detener = True

