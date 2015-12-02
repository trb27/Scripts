#!/usr/bin/env python

"""Script de ADF para obtener el esquema Nalewajski
@author: Tiare R
Ejecutar:
  ./nalewajski.py archivo.out 
Tambien se puede de la siguiente forma:
 python nalewajski.py archivo.out
"""


import re
import sys
import os

def nalewajski(filename):
	palabra=re.compile(r"(B\sO\sN\sD\s-\sO\sR\sD\sE\sR\s*A\sN\sA\sL\sY\sS\sI\sS)")
	dista=re.compile(r"(\s*DIST.\s*\[A\]\s*BOND-ORDERS)")
	thes=re.compile(r"(\s*\(THRESHOLD\s=\s*\d+\.\d+\s*\))")
	total=re.compile(r"(\s*\d-CENTER\s*TOTAL\s*\(\*\))")
	form=re.compile(r"([A-Z]+\s*(\d+\s-\s[A-Z]+)\s*(\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+))")
	suma=re.compile(r"Sum\s*:\s*(\d+\.\d+)\s*(\d+\.\d+)")
	fecha=re.compile("(ADF\s*(\d+\.\d+)\s*RunTime:\s*(\w+\-\d+)\s*(\d+:\d+:\d+)\s*Nodes:\s*(\d+)\s*Procs:\s*(\d+))")
	(nombreF, ext)=os.path.splitext(filename)
	f = open(filename,'r')
	new=open("nalewajski_"+nombreF+".out",'w')
	
	while True:
		line = f.readline()
		if not line: break
		
		boa=palabra.search(line)
		d=dista.search(line)
		t=thes.search(line)
		centerT=total.search(line)
		end=form.search(line)
		s=suma.search(line)
		fe=fecha.search(line)
		if fe!=None:
			fech=fe.group(3)
		if boa != None:
			new.writelines(boa.group(0)+"\n")
			new.write("===================================================="+"\n")
			
		if d != None:
			new.writelines(d.group(0)+"\n")
			new.write("-----------------------------------------------------------"+"\n")
			
		if t != None:
			new.writelines(t.group(0)+"\n")
			new.write("-----------------------------------------------------------"+"\n")
			
		if centerT != None:
			new.writelines(centerT.group(0)+"\n")
			new.write("-----------------------------------------------------------"+"\n")
			
		if end != None:
			new.writelines(end.group(0)+"\n")
			
		if s != None:
			new.write("-----------------------------------------------------------"+"\n")
			new.writelines(s.group(0)+"\n")
	print fech		
	new.close()
	
  

if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		nalewajski(filename)
		
	else:
		print "Usage: python {} somefile.out"
		sys.exit(1)
		
	
