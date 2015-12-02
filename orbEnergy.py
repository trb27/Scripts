#!/usr/bin/env python

"""
Script para ADF para saber la energia de un orbital
dado el nombre del fragmento y la etiqueta del orbital.
@author: Tiare R	
Ejecutar:
./correlacion.py archivo.out grupo etiqueta
el grupo es el fragmento por ejemplo Graph_nh2 y la etiqueta es el numero
del orbital por ejemplo 2
Tambien se puede ejecutar:
python correlacion.py archivo.out grupo etiqueta


"""

import re
import sys


def correlacion(filename,et,num):
    corr=re.compile("((\d+)\s*(\d+)\s*((-)*|(\d+\.\d+))\s*(-?\d+\.\d+)\s*(au)\s*%s\s*(\d+\.\d+)\s*%s\s*([A-Za-z]+)\s*(\d+))"%(et,num))
    f = open(filename)
	
    while True:
		line = f.readline()
		if not line: break
		n=corr.search(line)
		
		if n != None:
			ni=n.group(7)
			aux=float(ni)
			print aux
			break


if __name__ == '__main__':
    if len(sys.argv) > 3:
		filename = sys.argv[1]
		eti=sys.argv[2]
		num=sys.argv[3]
		correlacion(filename,eti,num)
		
    else:
		print "Usage: python {} somefile.out fragment orbital"
		sys.exit(1)
		
    

