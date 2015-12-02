#!/usr/bin/env python

"""Script de GULP para graficar tiempo,
 energia total, temperatura, presion
@author: Tiare R
Ejecutar:
  ./Graficar_gulp.py archivo.gout

Tambien se puede de la siguiente forma:
 python Graficar_gulp.py archivo.gout
 Este script necesita del modulo matplotlib, si no lo tienen instalado
 pueden instalarlo de la siguiente forma: 
 pip install matplotlib
"""


import re
import sys
import os
from matplotlib import pyplot
import psycopg2



conn = psycopg2.connect("dbname=ier user=ier password=ier host=localhost")
cur = conn.cursor()


def mdpG(filename):
	palabra1=re.compile(r"(Molecular\sdynamics\sproduction\s:\n)")
	tiempo=re.compile("(\*\*\s*Time\s*:\s*(\d+\.\d+)\s*ps\s*:)")
	total_energy=re.compile("((Total energy\s*\(eV\))\s=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	temperature=re.compile("((Temperature\s*\(K\))\s*=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	pression=re.compile("((Pressure\s*\(GPa\))\s*=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	fecha=re.compile("(Job Started  at\s*(\d+:\d+\.\d+)\s*(\d+\w+\s*\w+\s*\d+))")
	(nombreF, ext)=os.path.splitext(filename)
	f = open(filename)
	save_path = "/home/Escritorio/Resultados/GULP/" #cambiar path
	completeName = os.path.join(save_path, "ext_"+nombreF)    
	new=open(completeName,'w')
	new.write("#Tiempo  Energia total  Temperatura  Presion\n")
	fech=""
	while True:
		line = f.readline()
		if not line: break
		
		word=palabra1.search(line)
		fe=fecha.search(line)
		
		if fe!=None:
			fech=fe.group(3)
			
		if word != None:
			#new.write(word.group(0)+"\n")
			while True:
				line=f.readline()
				t=tiempo.search(line)
				te=total_energy.search(line)
				tmp=temperature.search(line)
				p=pression.search(line)
				if t!= None:
					ti=t.group(2)
					aux=float(ti)
					time.append(aux)
					new.write(t.group(2)+" ")
				if te!=None:
					to=te.group(3)
					aux2=float(to)
					tener.append(aux2)
					new.write(te.group(3)+" ")
				if tmp!=None:
					tem=tmp.group(3)
					aux3=float(tem)
					temp.append(aux3)
					new.write(tmp.group(3)+" ")
				if p!=None:
					pres=p.group(3)
					aux4=float(pres)
					pr.append(aux4)
					new.write(p.group(3)+"\n")
				if not line:break
	new.close()	
	
	
	
	

def Graficar():
	T_a,Ti_a,E_a,P_a,nombre,f=mdpG(filename)
	pyplot.figure()
	pyplot.plot(Ti_a,T_a)
	pyplot.title("Temperatura vs Tiempo "+nombre)
	pyplot.xlabel("Tiempo")
	pyplot.ylabel("Temperatura")
	pyplot.savefig("1"+nombre+".png")
	pyplot.figure()
	pyplot.plot(Ti_a,E_a)
	pyplot.title("Energia vs Tiempo "+nombre)
	pyplot.xlabel("Tiempo")
	pyplot.ylabel("Energia")
	pyplot.savefig("2"+nombre+".png")
	pyplot.figure()
	pyplot.plot(T_a,E_a)
	pyplot.title("Energia vs Temperatura "+nombre)
	pyplot.xlabel("Temperatura")
	pyplot.ylabel("Energia")
	pyplot.savefig("3"+nombre+".png")
	pyplot.figure()
	pyplot.plot(T_a,P_a)
	pyplot.title("Presion vs Temperatura "+nombre)
	pyplot.xlabel("Temperatura")
	pyplot.ylabel("Presion")
	pyplot.savefig("4"+nombre+".png")
	pyplot.figure()
	pyplot.plot(Ti_a,P_a)
	pyplot.title("Presion vs Tiempo "+nombre)
	pyplot.xlabel("Tiempo")
	pyplot.ylabel("Presion")
	pyplot.savefig("5"+nombre+".png")
	#print f #fecha

	


if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		mdpG(filename)
		#Graficar()
	else:
		print "Usage: python {} somefile.gout"
		sys.exit(1)
