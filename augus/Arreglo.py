import sys
sys.path.append('./augus')
from ArbolCaracteres import ArbolCaracteres
class Arreglo:
    def __init__(self):
        self.diccionario = {}
    #Direcciones es un arreglo de indices {0:{Nombre:"Daniel", Direccion: "Zona 4", Telefono:{0:56457854,1:48457585}}}
    #valor es el valor que se desea guardar
    def add(self,direcciones, valor):
        self.__add3(0,direcciones,valor,self.diccionario)

    def __add3(self,indice,direcciones,valor, diccionario):
        if isinstance(diccionario,dict):
            if not direcciones[indice] in diccionario:
                new_dic = {}
                diccionario[direcciones[indice]] = new_dic
                if indice +1 < len(direcciones):
                    self.__add3(indice+1,direcciones,valor,diccionario[direcciones[indice]])
                else:
                    diccionario[direcciones[indice]] = valor
            else:
                self.__add3(indice+1,direcciones,valor,diccionario[direcciones[indice]])
    def firstElement(self,diccionario):
        for index in diccionario.values():
            return index
    
    def exist(self, direcciones):
        return self.__existeIndex(0,direcciones,self.diccionario)

    def __existeIndex(self, indice, direcciones, diccionario):
        if isinstance(diccionario,dict):
            if direcciones[indice] in diccionario:
                if indice +1< len(direcciones): 
                    return self.__existeIndex(indice+1, direcciones,diccionario[direcciones[indice]])
            else:
                return False
        else:
            if indice+1==len(direcciones):
                if(diccionario, ArbolCaracteres):
                    return False

        return True

    def isThree(self,direcciones):
        return self.__lastElement(0, direcciones,self.diccionario)

    def __lastElement(self,indice,direcciones, diccionario):
        if isinstance(diccionario,dict):
            if direcciones[indice] in diccionario:
                if indice+1 < len(direcciones):
                    return self.__lastElement(indice+1, direcciones, diccionario[direcciones[indice]])
        else:
            if isinstance(diccionario,ArbolCaracteres):
                return True
        return False

    def setChars(self, direcciones, value):
        self.__chars(0, direcciones,value, self.diccionario)
    
    def __chars(self, indice, direcciones, value, diccionario):
        if isinstance(diccionario,dict):
            if direcciones[indice] in diccionario:
                if indice+1 < len(direcciones):
                    return self.__chars(indice+1, direcciones,value, diccionario[direcciones[indice]])
        else:
            if isinstance(direcciones[indice],int):
                diccionario.setChar(direcciones[indice],value)
                return True
        return False
                

    def getValue(self,direcciones):
        return self.__get(0,direcciones, self.diccionario)

    def __get(self,index, direcciones, diccionario):
        if (index+1)==len(direcciones):
            return diccionario[direcciones[index]]
        else:
            return self.__get(index+1, direcciones, diccionario[direcciones[index]])

    def setValue(self, direcciones, value):
        self.__set(0,direcciones,value,self.diccionario)
    def __set(self,index, direcciones, value, diccionario):
        if (index+1)==len(direcciones):
            diccionario[direcciones[index]]=value
        else:
            self.__set(index+1, direcciones, value, diccionario[direcciones[index]])
        