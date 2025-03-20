def quicksort(lista):
    if len(lista) <= 1:
        return lista

    pivote = lista[len(lista) // 2]

    izquierda = [x for x in lista if x < pivote]
    medio = [x for x in lista if x == pivote]
    derecha = [x for x in lista if x > pivote]

    return quicksort(izquierda) + medio + quicksort(derecha)

numeros = [5, 3, 8, 4, 2, 9, 1]
print(quicksort(numeros))
