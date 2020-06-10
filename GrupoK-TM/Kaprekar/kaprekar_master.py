from kaprekar_mostrarResultado import mostrarResultado
from kaprekar_ascendente import ascendente
from kaprekar_descendente import descencente

casosDePrueba = int(input("Cuantos numeros desea testear? "))
caso=0

while(caso<casosDePrueba):
	n = input("\nIngresa un numero de 4 digitos: ")
	# Compruebo que tenga al menos 2 cifras diferentes
	# Comprueba que no tenga mas de 4 cifras en total
	# Comprueba que no sea un numero negativo
	while(int(n)<0 or int(n)>9998):
		n = input("Ingreso incorrecto!! Ingrese nuevamente: ")

	
	contador = 0
	if int(n)%1111==0:
		print("DEBE CONTENER, AL MENOS DOS CIFRAS DIFERENTES!!")
		caso+=1
	elif n=="6174":
		print("Numero ingresado es la constante")
		caso+=1
	else:
		# bucle con contador que ordena los métodos y realiza la operación:
		print ("\nOrdenando ", n)
		while n != 6174:
			nDes = int(descencente(n))
			nAsc = int(ascendente(n))
			n = nDes - nAsc
			print(nDes," - ",nAsc," = ", n)
			contador+=1
		mostrarResultado(n,contador)
		caso+=1
	print("--------------------------------------------")
	print("Intento numero: ",caso," de ",casosDePrueba)
	print("--------------------------------------------")
