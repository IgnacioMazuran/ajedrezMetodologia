# Ordena en forma descendente
# Completa con 0 si tiene menos de 4 cifras
def descencente(n):
	num = str(n)

	if len(num)==4:
		sNum = num
	elif len(num)==3:
		sNum = num+"0"
	elif len(num)==2:
		sNum = num+"00"
	elif len(num)==1:
		sNum = num+"000"

	sNum = ''.join(sorted(str(sNum))[::-1])
	return sNum
