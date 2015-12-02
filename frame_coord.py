#!/usr/bin/env python

"""Script LAMMPS para obtener frames especificos de 
coordenadas atomicas, con el atomo etiquetado como 1
que hace referencia al carbono.
@author: Tiare R
Ejecutar:
  ./frame_coord.py archivo.out numero
numero es un entero positivo 
Tambien se puede de la siguiente forma:
 python frame_coord.py archivo.out numero
"""


import re
import sys
import os

def frameN(filename,num):
	palabra=re.compile(r"Atoms\.\s*Timestep:\s*%s\n"%num)
	coord=re.compile("(1)\s+((-?\d+\.\d+(e-\d+)?)|(-?\d+))\s+((-?\d+\.\d+(e-\d+)?)|(-?\d+))\s+((-?\d+\.\d+(e-\d+)?)|(-?\d+))")
	(nombreF, ext)=os.path.splitext(filename)
	f = open(filename)
	new=open(num+"_"+nombreF+".xyz",'w')
	le=f.readline()
	auxL=str(le)
	new.write(auxL)
	while True:
		line = f.readline()
		if not line: break

		word=palabra.match(line)	
		if word != None:
			new.write("#"+word.group(0))
			line=f.readline()
			aux=coord.search(line)
			while aux != None:
				aux1=aux.group(1)
				aux1="C"
				new.writelines(aux1+" "+aux.group(2)+" "+aux.group(6)+" "+aux.group(10)+"\n")
				line=f.readline()
				aux=coord.search(line)
			
		
	    
	new.close()
    

if __name__ == '__main__':
	if len(sys.argv) > 2:
		filename = sys.argv[1]
		num= sys.argv[2]
		frameN(filename,num)
    
	else:
		print "Usage: python {} somefile.out"
		print "miss number of iteration "
		sys.exit(1)
	
