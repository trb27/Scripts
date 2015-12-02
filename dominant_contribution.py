#!/usr/bin/env python

"""
Script de Turbomole para obtener estados excitados
@author: Tiare R
Ejecutar:
  ./dominant_contribution archivo archivo2.out
El primer archivo sera el archivo "spectrum" y el segundo con extension.out
Tambien se puede de la siguiente forma:
 python dominant_contribution.py archivo archivo2.out
"""



import re
import sys
import os
 
 
def return_lista(filename):
	archivo=open(filename, 'r')
	spec=re.compile(r"((-?\d+\.\d*E-?\+?\d+)\s*(-?\d+\.\d*E-?\+?\d+))")
	lista_edo=[]
	lista_lo=[]
	
	while True:
		line=archivo.readline()
		if not line: break
		
		p=spec.search(line)
		if p != None:
			n=p.group(3)
			aux=float(n)
			lista_edo.append(aux)
			mu=p.group(2)
			aux1=float(mu)
			lista_lo.append(aux1)
			
	return lista_lo, lista_edo

def singleExcitation(filename,num,longw,fuerza):
	fecha = re.compile(r"(\s+(\d+\-\d+\-\d+)\s*(\d+:\d+:\d+\.\d+))")
	convergencia = re.compile("(\w+\s*:\s*all\s*done)")
	single_excitation = re.compile(r"((%s)\s*(singlet a excitation))"%num)
	excitation_energy = re.compile(r"((Excitation energy / eV:)\s*(-?\d+\.\d+))")
	dominant_contribution = re.compile(r"((-?\d+\s*[a-z])\s*(-?\d+\.\d+)\s*(-?\d+\s*[a-z])\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
	dominant_more=re.compile(r"(occ\.\s*orbital\s*energy\s*/\s*eV\s*virt\.\s*orbital\s*energy\s/\s*eV\s*\|coeff\.\|\^\d+\*\d+)")
	electric_transition = re.compile(r"(Electric transition dipole moment \(length rep\.\))")
	elec_tran_x = re.compile(r"((x)\s*(-?\d+\.\d+)\s*(Norm:)\s*(-?\d+\.\d+))")
	elec_tran_y = re.compile(r"((y)\s*(-?\d+\.\d+))")
	elec_tran_z = re.compile(r"((z)\s*(-?\d+\.\d+)\s*(Norm / debye:)\s*(-?\d+\.\d+))")
	quadrupole=re.compile(r"\s*Electric quadrupole transition moment:")
	q_x=re.compile(r"((\s*xx)\s*(-?\d+\.\d+))")
	q_y=re.compile(r"((\s*yy)\s*(-?\d+\.\d+)\s*(1/3\*trace:)\s*(-?\d+\.\d+))")
	q_z=re.compile(r"((\s*zz)\s*(-?\d+\.\d+))")
	q_xy=re.compile(r"((\s*xy)\s*(-?\d+\.\d+))")
	q_xz=re.compile(r"((\s*xz)\s*(-?\d+\.\d+)\s*(Anisotropy:)\s*(-?\d+\.\d*))")
	q_yz=re.compile(r"((\s*yz)\s*(-?\d+\.\d+))")
	(nombreF, ext) = os.path.splitext(filename)
	f = open(filename,'r')
	new = open("estados_excitados_"+nombreF+".dat",'w')
	numeroMayor=str(num)
	longitud_onda=str(longw)
	fuerza_os=str(fuerza)
	new.write("Estado exitado\t Longitud de onda\t Fuerza de oscilador\t Energia Exitada\n")
	new.write(numeroMayor+"\t\t"+longitud_onda+"\t\t"+fuerza_os)
	
	while True:
		line = f.readline()
		if not line: break
		se=single_excitation.search(line)
		conv=convergencia.search(line)
		
		if conv!=None:
			print (conv.group(0))
			line=f.readline()
			line=f.readline()
			line=f.readline()
			fec=fecha.search(line)
			if fec!=None:
				print (fec.group(2))
		if se!=None:
			#new.write(se.group(0)+"\n")
			c=True
			while (c==True):
				line=f.readline()
				ee=excitation_energy.search(line)
				dc=dominant_contribution.search(line)
				dm=dominant_more.search(line)
				et=electric_transition.search(line)
				q=quadrupole.search(line)
				if ee!=None:
					new.write("\t\t"+ee.group(3)+"\n\n")
				if dm!=None:
					new.write("Dominant contributions:\n")
					new.write(dm.group(0)+"\n")
				if dc!=None:
					new.write(dc.group(0)+"\n\n")
				if et!=None:
					new.write(et.group(0)+"\n")
					line=f.readline()
					line=f.readline()
					etx=elec_tran_x.search(line)
					if etx!=None:
						new.write(etx.group(0)+"\n")
						line=f.readline()
						ety=elec_tran_y.search(line)
						if ety!=None:
							new.write(ety.group(0)+"\n")
							line=f.readline()
							etz=elec_tran_z.search(line)
							if etz!=None:
								new.write(etz.group(0)+"\n\n")	
					
				if q!=None:
					new.write(q.group(0)+"\n")
					line=f.readline()
					line=f.readline()
					qx=q_x.search(line)
					if qx!=None:
						new.write(qx.group(0)+"\n")
						line=f.readline()
						qy=q_y.search(line)
						if qy!=None:
							new.write(qy.group(0)+"\n")
							line=f.readline()
							qz=q_z.search(line)
							if qz!=None:
								new.write(qz.group(0)+"\n")
								line=f.readline()
								qxy=q_xy.search(line)
								if qxy!=None:
									new.write(qxy.group(0)+"\n")
									line=f.readline()
									qxz=q_xz.search(line)
									if qxz!=None:
										new.write(qxz.group(0)+"\n")
										line=f.readline()
										qyz=q_yz.search(line)
										if qyz!=None:
											new.write(qyz.group(0))
					c=False
	new.close()
	
	
	
if __name__ == '__main__':
	if len(sys.argv)>2:
		filename1=sys.argv[1]
		filename2=sys.argv[2]
		lista1,lista2=return_lista(filename1)
		numM=max(lista2)
		pos=lista2.index(numM)
		n=pos+1
		longwave=lista1[pos]
		singleExcitation(filename2,n,longwave,numM)
		
	else:
		print "Usage: python {} archivo somefile.out"
		sys.exit(1)
