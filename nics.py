#!/usr/bin/env python

"""Script de Gaussian para obtener nics
@author: Tiare R
Ejecutar:
  ./nics.py archivo.log 
Tambien se puede de la siguiente forma:
 python nics.py archivo.log
"""


import re
import sys
import os

def nics(filename):
    nics1=re.compile(r"((\d+)\s*(Bq)\s*(Isotropic\s*=)\s*(-?\d+.\d+)\s*(Anisotropy\s*=)\s*(-?\d+.\d+))")
    conv=re.compile(r"(Normal termination of Gaussian \d+ at (\w+\s+\w+\s+\d+)\s+(\d+:\d+:\d+)\s+(\d+))")
    (nombreF, ext)=os.path.splitext(filename)
    f = open(filename,'r')
    c="No convergio"
    while True:
		line = f.readline()
		if not line: break
		n=nics1.search(line)
		co=conv.search(line)
		if n != None:
			ni=n.group(5)
			aux=float(ni)
			print aux
			if aux > 0: print "Es aromatica"
			elif aux == 0: print "No es aromatica"
			else: print "Es antiaromatica"
		if co!=None:
			c="Convergio"	
			print c
			print (co.group(2))
			
if __name__ == '__main__':
    if len(sys.argv) > 1:
	filename = sys.argv[1]
	nics(filename)
    else:
		print "Usage: python {} somefile.log"
		sys.exit(1)
		
    
