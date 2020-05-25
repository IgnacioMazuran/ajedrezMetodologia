
# Ordena en forma ascendente
from ascendente import ascendente

# Ordena en forma descendente

from descendente import descendente
# Solicita el numero al usuario
from ingresoNum import ingresoNum

# Bucle con contador
contador = 0
# Llamada a los métodos en orden
while n != descendente(n) - ascendente(n):
    print (descendente(n), "-", ascendente(n), "=", descendente(n)-ascendente(n))
    n = descendente(n) - ascendente(n)
    contador+=1

print ("Se alcanzó la constante de Kaprekar: ", n, " en ",contador," vueltas")
