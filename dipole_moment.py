#!/usr/bin/env python

"""
Scrip de Turbomole para obtener momentos dipolares
@author: Tiare R
Ejecutar:
  ./dipole_moment.py archivo.last

Tambien se puede de la siguiente forma:
 python dipole_moment.py archivo.out
"""

import re
import sys
import os

def dipole_moment(filename):
	fecha = re.compile(r"(\s+(\d+\-\d+\-\d+)\s*(\d+:\d+:\d+\.\d+))")
	convergencia = re.compile("(\w+\s*:\s*all\s*done)")
	dipole=re.compile(r"(\s*dipole\s*moment\s*\n)")
	cx=re.compile(r"((\s+x)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	cy=re.compile(r"((\s+y)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	cz=re.compile(r"((\s+z)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	dip_mom=re.compile(r"((\|\s*dipole\s*moment\s*\|)\s*(=)\s*(-?\d+\.\d+)\s*([A-Za-z]\.[A-Za-z]\.\s*=)\s*(-?\d+\.\d+)\s*(debye))")
	(nombreF, ext)=os.path.splitext(filename)
	f = open(filename)
	new=open("dipole_moment_"+nombreF+".dat",'w')
	new.write("X\t\t Y\t\t Z\t\t Dipole moment\n")	
	while True:
		line = f.readline()
		if not line: break
							
		d=dipole.search(line)

		if d != None:
			#new.writelines(d.group(0)+"\n")
			while True:
				line=f.readline()
				x=cx.search(line)
				y=cy.search(line)
				z=cz.search(line)
				dp=dip_mom.search(line)
				conv=convergencia.search(line)
				if x != None:
					new.write(x.group(5)+"\t")
						
				if y != None:
					new.write(y.group(5)+"\t")
						
				if z != None:
					new.write(z.group(5)+"\t")
						
				if dp != None:
					new.write(dp.group(6)+"\n")
					
				if conv!=None:
					print (conv.group(0))
					line=f.readline()
					line=f.readline()
					line=f.readline()
					fec=fecha.search(line)
					if fec!=None:
						print (fec.group(2))
			
				if not line: break
		
			
	new.close()
				
				
				
						
if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		dipole_moment(filename)
					
	else:
		print "Usage: python {} somefile.last"
		sys.exit(1)
					
	
