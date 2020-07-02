import threading
import time
import re
from TablaSimbolo import *
from augus.HilosGraficar import Graficar3D
from augus.Ejecutar import Ejecutor
import augus.GramaticaA as GramaticaA
from augus.Recolectar import Recolectar
from augus.TablaSimbolosA import TablaSimbolosA as TSA

class Optimizacion(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.etiquetas = args[0]
        self.C3D = args[1]
        self.consola = args[2]
        self.GTS = args[3]
        self.codigo = ""
        self.optimizadas = []
        self.in_console = None

    def setParams(self, linea, estado):
        self.in_console.setParams(linea,estado)

    def imprimir3D(self):
        self.codigo = ""
        for etiqueta in self.etiquetas:
            self.C3D.addItem(etiqueta+":")
            self.codigo += etiqueta+":\n" 
            for cuadruplo in self.etiquetas[etiqueta]:
                if cuadruplo.op == "if":
                    self.C3D.addItem(" if({0}) goto {1};".format(cuadruplo.arg1, cuadruplo.result))
                    self.codigo+=" if({0}) goto {1};".format(cuadruplo.arg1, cuadruplo.result)
                elif cuadruplo.op == "goto":
                    self.C3D.addItem(" goto {0};".format(cuadruplo.arg1))
                    self.codigo+=" goto {0};".format(cuadruplo.arg1)
                elif cuadruplo.op == "print":
                    self.C3D.addItem("  print({0});".format(cuadruplo.arg1))
                    self.codigo+=" print({0});".format(cuadruplo.arg1)
                elif cuadruplo.op == "exit":
                    self.C3D.addItem("  exit;")
                    self.codigo+=" exit;"
                elif cuadruplo.op != "=":
                    self.C3D.addItem(" {0}={1} {2} {3};".format(cuadruplo.result,cuadruplo.arg1, cuadruplo.op, cuadruplo.arg2))
                    self.codigo+= " {0}={1} {2} {3};".format(cuadruplo.result,cuadruplo.arg1, cuadruplo.op, cuadruplo.arg2)
                else:
                    self.C3D.addItem(" {0}={1}{2};".format(cuadruplo.result,cuadruplo.arg1,cuadruplo.arg2))
                    self.codigo+=" {0}={1}{2};".format(cuadruplo.result,cuadruplo.arg1,cuadruplo.arg2)
                self.codigo+="\n"
            self.C3D.addItem("")
            self.codigo+="\n"
    
    def run(self):
        self.optimizadas = []
        'regla 1'
        self.etiquetas = self.regla1()
        'regla 2'
        self.etiquetas = self.regla2()
        'regla 3'
        self.etiquetas = self.regla3()
        'regla 3'
        self.etiquetas = self.regla3(pasada =1)
        'regla 4'
        self.etiquetas = self.regla4()
        'regla 2'
        self.etiquetas = self.regla2()
        'regla 5'
        self.etiquetas = self.regla5()
        'regla 2'
        self.etiquetas = self.regla2()
        #-----------------------#
        self.imprimir3D()
        self.analizar()
        #print(self.codigo)
        #print(self.optimizadas)
        g3d = Graficar3D(args=(self.optimizadas,"reporteOptimizado"),daemon= True)
        g3d.start()

    def analizar(self):
            ast2 = GramaticaA.parse(self.codigo)
            ast3 = ast2.instruccion
            ts = TSA()
            recolector = Recolectar(ast3,ts,[])
            recolector.procesar()
            self.in_console = Ejecutor(args=(ast3,ts,[],"",self.consola, self.GTS),daemon=True)
            self.in_console.start()
    
    def regla1(self):
        etiquetas = {}
        cambios = {}
        for etiqueta in self.etiquetas:
            etiquetas[etiqueta] = []
            for cuadruplo in self.etiquetas[etiqueta]:
                ''#debemos ir buscando op con =
                pattern = r'(\$t[0-9]+)'
                match1 = re.match(pattern,str(cuadruplo.arg1))
                if cuadruplo.op == "=" and match1:
                    if len(etiquetas[etiqueta])!=0:
                        ant = etiquetas[etiqueta].pop()
                        if ant.result == cuadruplo.arg1 and (not '[' in cuadruplo.result) and (cuadruplo.arg2 !=" "):
                            self.add(ant,1)
                            cambios[ant.result] = cuadruplo.result
                            new = Cuadruplo(ant.op,ant.arg1,ant.arg2,cuadruplo.result)
                            etiquetas[etiqueta].append(new)
                            continue
                        else:
                            etiquetas[etiqueta].append(ant)
                        

                etiquetas[etiqueta].append(cuadruplo)

        return etiquetas
    
    def regla2(self):
        #objeto para almacenar etiquetas 
        etiquetas = {}
        eliminar = False
        for etiqueta in self.etiquetas:
            etiquetas[etiqueta] = []
            eliminar = False

            for cuadruplo in self.etiquetas[etiqueta]:
                if eliminar:
                    self.add(cuadruplo, 2)
                    continue
                if cuadruplo.op == "goto":
                    etiquetas[etiqueta].append(cuadruplo)
                    eliminar = True
                else:
                    etiquetas[etiqueta].append(cuadruplo)

        return etiquetas

    #Region para regla 3
    def regla3(self, pasada = 0):
        etiquetas = {}
        eliminadas = {}
        flag = False
        for etiqueta in self.etiquetas:
            if  not etiqueta in eliminadas:
                etiquetas[etiqueta] = []

                for i in range(len(self.etiquetas[etiqueta])):
                    if flag:
                        flag = False
                    else:
                        if self.etiquetas[etiqueta][i].op == "if":
                            if 0 != len(etiquetas[etiqueta]):
                                if i+1 < len(self.etiquetas[etiqueta]):
                                    if self.etiquetas[etiqueta][i+1].op == "goto":
                                        cuadruplo = etiquetas[etiqueta].pop()
                                        _if = self.etiquetas[etiqueta][i].result
                                        goto_end = self.etiquetas[etiqueta][i+1]
                                        #generamos el nuevo if (negacion ) goto end
                                        new = self.generarIf(cuadruplo, goto_end.arg1)
                                        if not self.canChange(cuadruplo):
                                            etiquetas[etiqueta].append(cuadruplo)
                                        else:
                                            self.add(cuadruplo,3)
                                        etiquetas[etiqueta].append(new)
                                        eliminadas[_if]=goto_end.arg1
                                        #obtendria todas las instrucciones del if
                                        for item in self.etiquetas[_if]:
                                            etiquetas[etiqueta].append(item)
                                        flag = True
                                        continue
                                    elif pasada == 0:
                                        cuadruplo = etiquetas[etiqueta].pop()
                                        self.add(cuadruplo,3)
                                        new = Cuadruplo("if", "{0}{1}{2}".format( cuadruplo.arg1, cuadruplo.op, cuadruplo.arg2),"goto" ,self.etiquetas[etiqueta][i].result)
                                        etiquetas[etiqueta].append(new)
                                        continue

                        etiquetas[etiqueta].append(self.etiquetas[etiqueta][i])


            else:
                etiquetas[etiqueta] = []
                #for cuadruplo in self.etiquetas[etiqueta]:
                    #self.add(cuadruplo,3)
        #una vez terminado el proceso seguimos a eliminar las etiquetas que cambiaron
        for etiqueta in eliminadas:
            self.add(etiqueta + ":",6)
            del etiquetas[etiqueta]
        #recorremos la lista de nuevo en busca de if y goto que puedan tener las etiquetas
        for salto in eliminadas:
            for etiqueta in etiquetas:
                for cuadruplo in etiquetas[etiqueta]:
                    if cuadruplo.op == "if":
                        if cuadruplo.result == salto:
                            cuadruplo.result = eliminadas[salto]
                    elif cuadruplo.op == "goto":
                        if cuadruplo.arg1 == salto:
                            cuadruplo.arg1 = eliminadas[salto]

        return etiquetas
    def canChange(self,cuadruplo):
        op = cuadruplo.op
        change = False
        if op == ">":
            op = "<="
            change = True
        elif op == "<":
            op= ">="
            change = True
        elif op == ">=":
            op = "<"
            change = True
        elif op == "<=":
            op = ">"
            change = True
        elif op == "==":
            op = "!="
            change = True
        elif op =="!=":
            op  = "=="
            change = True
        return change
    def generarIf(self,cuadruplo, goto_end):
        op = cuadruplo.op
        change = False
        if op == '>':
            op = '<='
            change = True
        elif op == '<':
            op= '>='
            change = True
        elif op == '>=':
            op = '<'
            change = True
        elif op == '<=':
            op = '>'
            change = True
        elif op == '==':
            op = '!='
            change = True
        elif op =='!=':
            op  = '=='
            change = True
        
        if change:
            return Cuadruplo("if", "{0}{1}{2}".format( cuadruplo.arg1, op, cuadruplo.arg2),"goto" ,goto_end)
        else:
            return Cuadruplo("if","!"+cuadruplo.result,"goto",goto_end)
    #End Region para regla 3
    def regla4(self):
        etiquetas = {}
        for etiqueta in self.etiquetas:
            etiquetas[etiqueta] = []
            for cuadruplo in self.etiquetas[etiqueta]:
                ''
                if cuadruplo.op == "if":
                    ''
                    if cuadruplo.arg1 == "1==1":
                        ''
                        new_cuadruplo = Cuadruplo("goto", cuadruplo.result,"","")
                        etiquetas[etiqueta].append(new_cuadruplo)
                        self.add(cuadruplo, 4)
                        continue
                etiquetas[etiqueta].append(cuadruplo)

        return etiquetas

    def regla5(self):
        etiquetas = {}
        for etiqueta in self.etiquetas:
            etiquetas[etiqueta] = []
            for i in range(len(self.etiquetas[etiqueta])):
                ''
                if self.etiquetas[etiqueta][i].op == "if":
                    ''
                    if self.etiquetas[etiqueta][i].arg1 == "1==0":
                        ''
                        if i + 1 < len(self.etiquetas[etiqueta]):
                            ''
                            if self.etiquetas[etiqueta][i+1].op == "goto":
                                ''
                                new_cuadruplo = Cuadruplo("goto", self.etiquetas[etiqueta][i+1].arg1,"","")
                                etiquetas[etiqueta].append(new_cuadruplo)
                                self.add(self.etiquetas[etiqueta][i], 4)
                                continue
                            else:
                                ''
                        else:
                            ''
                    else:
                        ''
                etiquetas[etiqueta].append(self.etiquetas[etiqueta][i])
        return etiquetas
    
    def add(self, cuadruplo, regla):
        self.optimizadas.append({"linea":cuadruplo, "regla": regla})