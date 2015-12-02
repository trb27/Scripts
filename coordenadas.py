#!/usr/bin/env python

"""Script de FHI-AIMS para obtener coordenadas de atomos
@author: Tiare R
Ejecutar:
  ./coordenadas_1.py archivo.out 
Tambien se puede de la siguiente forma:
 python coordenadas_1.py archivo.out
"""


import re
import sys
import os

def coord(filename):
	n=re.compile(r"(Number of atoms\s*:?\s*(\d+))")
	coord=re.compile(r"atom\s*((-?\d+\.\d+\s*)(-?\d+\.\d+\s*)(-?\d+\.\d+\s*)([A-Za-z]+))")
	palabra=re.compile(r"Relaxation step number\s*\d+:")
	final=re.compile(r"Final atomic structure:")
	fecha=re.compile(r"(\s*Date\s*:\s*(\d+))")
	antesF=re.compile(r"(Leaving FHI-aims\.)")
	conv=re.compile(r"(Have a nice day\.)")
	(nombreF, ext)=os.path.splitext(filename)
	f = open(filename,'r')
	new=open("coord_"+nombreF+".out",'w')
	new.write("#\t\t x[A]\t\t y[A]\t\t z[A]\n")
	c="No convergio"
	while True:
		line = f.readline()
		if not line: break
		
		nA=n.search(line)
		word=palabra.search(line)
		aux=coord.search(line)
		end=final.search(line)
		aF=antesF.search(line)
		co=conv.search(line)
		if nA != None:
			new.writelines(nA.group(0)+"\n")
		
		if word != None:
			new.writelines(word.group(0)+"\n")
		
		if end != None:
			new.writelines(end.group(0)+"\n")
			
		if aux != None:
			new.writelines(aux.group(0)+"\n")
		if aF!=None:
			antF=aF.group(0)
			line=f.readline()
			fech=fecha.search(line)
			if fech!=None:
				fecha1=fech.group(2)
				#print fecha1
		if co!=None:
			c="Convergio"
			#print c
				
	new.close()
	
  

if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		coord(filename)
    
	else:
		print "Usage: python {} somefile.out"
		sys.exit(1)
	
