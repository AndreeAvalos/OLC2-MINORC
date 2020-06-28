import threading
import subprocess
class GraficarArbol(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.nodo = args[0]
        self.name = args[1]

    def run(self):
        self.construirAST(self.nodo)

    def cmd(self, commando):
        subprocess.run(commando, shell=True)

    def construirAST(self,nodo):
        ruta = "{0}.dot".format(self.name)
        destino= "dot -Tpng {0}.dot -o {1}.png".format(self.name, self.name)
        try:
            file = open(ruta, "w")
            file.write("digraph{ \n")
            self.imprimirNodos(nodo,file)
            self.graficar(nodo,file)
            file.write("\n}")
            file.close()
        except:
            print("ERROR")
        finally:
            self.cmd(destino)

    def imprimirNodos(self,nodo,file):
        file.write(str(nodo.index)+"[style = \"filled\" ; label = \""+nodo.nombre+"\"] \n")
        if nodo.childs != None:
            for child in nodo.childs:
                self.imprimirNodos(child, file)

    def graficar(self, nodo,file):
        if nodo.childs != None:
            for child in nodo.childs:
                file.write(str(nodo.index)+"->"+str(child.index)+";\n")
                self.graficar(child,file)

class GraficarGramatica(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.lst = args[0]
        self.name = args[1]

    def run(self):
        self.construirReporteGramatical(self.lst)

    def cmd(self, commando):
        subprocess.run(commando, shell=True)

    def construirReporteGramatical(self, lstGrmaticales):
        ruta = "{0}.dot".format(self.name)
        destino= "dot -Tpng {0}.dot -o {1}.png".format(self.name, self.name)
        try:
            file = open(ruta, "w")
            file.write("digraph ReporteGramatical{\n")
            file.write("graph [ratio=fill];node [label=\"\\N\", fontsize=15, shape=plaintext];\n")
            file.write("graph [bb=\"0,0,352,154\"];\n")
            file.write("arset [label=<")
            file.write("<TABLE ALIGN=\"LEFT\">\n")
            file.write("<TR><TD>Produccion</TD><TD>Reglas Semanticas</TD></TR>\n")
            for nodo in lstGrmaticales:
                file.write("<TR>")
                file.write("<TD>")
                file.write(nodo.produccion.replace("->",":"))
                file.write("</TD>")
                file.write("<TD><TABLE BORDER=\"0\">")
                for regla in nodo.reglas:
                    file.write("<TR><TD>")
                    file.write(regla)
                    file.write("</TD></TR>")
                file.write("</TABLE></TD>")
                file.write("</TR>\n")
            file.write("</TABLE>")
            file.write("\n>, ];\n")
            file.write("}")
        except:
            print("ERROR AL ESCRIBIR TABLA")
        finally:
            file.close()
            self.cmd(destino)
