def quiksort(numeros):
    if len(numeros) <=1:
        return numeros
    
    voti=numeros[len(numeros) // 2]
    
    derecha = [x for x in numeros if x < voti]
    medio = [x for x in numeros if x == voti]
    izquierda = [x for x in numeros if x > voti]
    
    return quiksort(derecha) + medio + quiksort(izquierda)

numeros=[8,3,8,5,4,7,1,9]
print(quiksort(numeros))