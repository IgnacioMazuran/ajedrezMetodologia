# Ordena el input del usuario en forma ascendente
# Completa con 0 si tiene menos de 4 cifras
def ascendente(n):
	num = str(n)
	
	if len(num)==4:
		sNum = num
	elif len(num)==3:
		sNum = "0"+num
	elif len(num)==2:
		sNum = "00"+num
	elif len(num)==1:
		sNum = "000"+num

	sNum = ''.join(sorted(str(sNum)))
	return sNum
    
    
