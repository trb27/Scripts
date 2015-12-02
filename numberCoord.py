#!/usr/bin/env python

"""Script de FHI-AIMS para obtener coordenadas especificas de atomos
@author: Tiare R
Ejecutar:
  ./numberCoord1.py archivo.out numero
el archivo tiene que ser coordenadas_origen  
numero es un entero positivo 
Tambien se puede de la siguiente forma:
 python numberCoord1.py archivo.out numero
"""


import re
import sys
import os

def coordN(filename,num):
	n=re.compile(r"(Number of atoms\s*:?\s*([0-9]+))")
	palabra=re.compile("Relaxation step number\s*%s:"%num)
	atom=re.compile("^atom")
	coord=re.compile(r"atom\s*((-?[0-9]*\.[0-9]+\s*)(-?[0-9]+\.[0-9]+\s*)(-?[0-9]+\.[0-9]+\s*)([A-Za-z]+))")
	(nombreF, ext)=os.path.splitext(filename)
	f = open(filename)
	new=open(num+"_C_FHI_"+nombreF,'w')
	new1=open(num+"_C_visual_"+nombreF+".xyz",'w')
	new.write("#\t\t x[A]\t\t y[A]\t\t z[A]\n")
	while True:
		try:
			line = f.readline()
			if not line: break
		
			nA=n.search(line)
			word=palabra.match(line)
		
			if nA != None:
				new1.writelines(nA.group(2)+"\n")
			
			
			if word != None:
				#new.writelines(word.group(0)+"\n")
				line=f.readline()
				aux=coord.search(line)
				while aux != None:
					new.write(aux.group(0)+"\n")
					new1.writelines(aux.group(5)+"\t"+aux.group(2)+"\t"+aux.group(3)+"\t"+aux.group(4)+"\n")
					line=f.readline()
					aux=coord.search(line)
				
		except ValueError:
			print "La coordenada deseada no existe..."
	
	    
	new.close()
	new1.close()
    

if __name__ == '__main__':
	if len(sys.argv) > 2:
		filename = sys.argv[1]
		num= sys.argv[2]
		coordN(filename,num)

    
	else:
		print "Usage: python {} somefile.out"
		print "miss number of iteration "
		sys.exit(1)
	
