#!/usr/bin/env python

"""Script de GULP para extraer tiempo, energia total, temperatura, presion
@author: Tiare R
Ejecutar:
  ./gulp.py archivo.out

Tambien se puede de la siguiente forma:
 python gulp.py archivo.out 
"""


import re
import sys
import os


def mdp(filename):
	palabra1=re.compile(r"(Molecular\sdynamics\sproduction\s:\n)")
	tiempo=re.compile("(\*\*\s*Time\s*:\s*(\d+\.\d+)\s*ps\s*:)")
	total_energy=re.compile("((Total energy\s*\(eV\))\s=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	temperature=re.compile("((Temperature\s*\(K\))\s*=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	pression=re.compile("((Pressure\s*\(GPa\))\s*=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	(nombreF, ext)=os.path.splitext(filename)
	f = open(filename)
	new=open("ext_"+nombreF+".dat",'w')
	new.write("#Tiempo  Energia total  Temperatura  Presion\n")
	while True:
		line = f.readline()
		if not line: break
		
		word=palabra1.search(line)
			
		if word != None:
			while True:
				line=f.readline()
				t=tiempo.search(line)
				te=total_energy.search(line)
				tmp=temperature.search(line)
				p=pression.search(line)
				if t!= None:
					new.write(t.group(2)+" ")
				if te!=None:
					new.write(te.group(3)+" ")
				if tmp!=None:
					new.write(tmp.group(3)+" ")
				if p!=None:
					new.write(p.group(3)+"\n")
				
				if not line:break		
				
	new.close()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		mdp(filename)
    
	else:
		print "Usage: python {} somefile.gout"
		sys.exit(1)
