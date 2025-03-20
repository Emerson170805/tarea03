def quiksort(numeros):
    if len(numeros) <=1:
        return numeros
    
    pilo = numeros[len(numeros) // 2]
    
    derecha = [x for x in numeros if x < pilo]
    medio = [x for x in numeros if x == pilo]
    izquierda = [x for x in numeros if x > pilo]
    
    return quiksort(derecha) + medio + quiksort(izquierda)

numeros=[6,8,7,3,5,4,7,2,9]
print(quiksort(numeros))