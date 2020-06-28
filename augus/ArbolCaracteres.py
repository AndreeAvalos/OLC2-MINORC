class ArbolCaracteres:
    #Metodo constructor para convertir la cadena en  arreglo de char
    def __init__(self, cadena):
        self.caracteres = []
        #parseamos los chars a una lista
        for x in range(len(cadena)):
            self.caracteres.append(cadena[x])
    #Metodo para obtener la cadena completa
    #Util para la impresion de valores
    def getText(self):
        salida = ""
        for x in range(len(self.caracteres)):
            salida+=self.caracteres[x]
        return salida
    #Metodo para agregar caracteres si el indice no existe 
    def setChar(self,num,char):
        #compara si se puede asignar el valor primero
        #De lo contrario es porque el index es mayor y se debe crear
        if len(self.caracteres)>num:
            self.caracteres[num] = char
        else:
            #obtenemos cuantos valores debemos insertar
            restante = num-len(self.caracteres)+1
            for x in range(restante):
                self.caracteres.append(" ")
            #asignamos el valor a su correspondiente indice
            self.caracteres[num] = char
    #Metodo que valida si se quiere ingresar a un indice mayor a la cantidad
    #de elementos del arreglo
    def valid(self, num):
        return True if(num+1<len(self.caracteres)) else False
    #Metodo que retorna un caracter por su indice
    def indexOf(self, num):
        return self.caracteres[num]
    


