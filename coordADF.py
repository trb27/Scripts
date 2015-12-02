#!/usr/bin/env python

"""
Script de ADF para obtener las ultimas coordenadas
@author: Tiare R
Ejecutar:
  ./coordADF archivo 
El archivo sera el archivo "logfile" 
Tambien se puede de la siguiente forma:
 python coordADF.py archivo 
 """

import os
import re
import sys




def coordADF(filename):
		n = re.compile(r"(\s+atoms:\s*(\d+)\s*\-\s*(\d+))")
		coord = re.compile(r"((\d+\.)([A-Za-z]+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
		palabra = re.compile(r"(GEOMETRY\s*CONVERGED)")
		(nombreF, ext)=os.path.splitext(filename)
		f = open(filename)
		new = open("coord_"+nombreF+".xyz", 'w')
		lista=[]
		while True:
			line = f.readline()
			if not line: break
		
			nA = n.search(line)
			word = palabra.search(line)
			
			
			if nA != None:
				lista.append(nA.group(3))
			
			if word != None:
				#new.writelines(word.group(0)+"\n")
				new.write(lista[0]+"\n")
				while True:
					line=f.readline()
					if not line: break
					aux = coord.search(line)
					if aux!=None:
						new.write(aux.group(3)+" "+aux.group(4)+" "+aux.group(5)+" "+aux.group(6)+"\n")
				
					
		new.close()
		
		
if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		coordADF(filename)
					
	else:
		print "Usage: python {} somefile"
		sys.exit(1)
					
			
	
