from kaprekar_mostrarResultado import mostrarResultado
from kaprekar_ascendente import ascendente
from kaprekar_descendente import descencente
# Bucle con contador
contador = 0

n = input("Ingresa un numero de 4 digitos: ")
print ("\nOrdenando ", n)

# Bucle con contador
contador = 0
# Llamada a los métodos en orden
while n != descencente(n) - ascendente(n):
    print (descencente(n), "-", ascendente(n), "=", descencente(n)-ascendente(n))
    n = descencente(n) - ascendente(n)
    contador+=1


mostrarResultado(n,contador)