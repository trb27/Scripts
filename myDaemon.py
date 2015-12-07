
"""
Script para monitorear el sistema de archivos
y almacenamiento de informacion en la base
de datos
@autor: Tiare R
Este script se va a ejecutar en background
con el comando nohup:
nohup python myDaemon.py &
"""

import os
import sys
import time
import re
import logging
import psycopg2
import Queue
import daemon
import pprint
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from matplotlib import pyplot


conn = psycopg2.connect("dbname=ier user=ier password=ier host=localhost")
cur = conn.cursor()

class MyHandler(PatternMatchingEventHandler):
	patterns = ["*.out", "*.log","*.gout","*.last"]
	
	def dipole_moment(self,f,nom,ruta):
		fecha = re.compile(r"(\s+(\d+\-\d+\-\d+)\s*(\d+:\d+:\d+\.\d+))")
		convergencia = re.compile("(\w+\s*:\s*all\s*done)")
		dipole=re.compile(r"(\s*dipole\s*moment\s*\n)")
		cx=re.compile(r"((\s+x)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
		cy=re.compile(r"((\s+y)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
		cz=re.compile(r"((\s+z)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
		dip_mom=re.compile(r"((\|\s*dipole\s*moment\s*\|)\s*(=)\s*(-?\d+\.\d+)\s*([A-Za-z]\.[A-Za-z]\.\s*=)\s*(-?\d+\.\d+)\s*(debye))")
		save_path = "/storage1/energy/Resultados/TURBOMOLE/"
		completeName = os.path.join(save_path, "dipole_moment_"+nom)         
		c1="No convergio"
		fech=""
		fecha1=""
		new = open(completeName, 'w')
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
						#print (conv.group(0))
						c1="Si convergio"
						line=f.readline()
						line=f.readline()
						line=f.readline()
						fech=fecha.search(line)
						if fech!=None:
							fecha1=fech.group(2)
							#print (fech.group(2))
				
					if not line: break
			
				
		new.close()
		try:
			new=open(completeName, 'r').read()
			binaryF = f.read()
			cur.execute("INSERT INTO turbomole(archivo,titulo,fecha,convergencia,dipole_moment,path) VALUES (%s,%s,%s,%s,%s,%s)", (psycopg2.Binary(binaryF),nom,fecha1,c1,new,ruta))
			conn.commit()
			f.close()
			
		except psycopg2.DatabaseError, dbe:
			print str(dbe)
			return(None)
		except Exception, e:
			print str(e)
			return(None)
				
	
	
	def coordenadas(self,f,nom,ruta):
		n = re.compile(r"(Number of atoms\s*:?\s*(\d+))")
		coord = re.compile(r"atom\s*((-?\d*\.\d+\s*)(-?\d+\.\d+\s*)(-?\d+\.\d+\s*)([A-Za-z]+))")
		palabra = re.compile(r"Relaxation step number\s*\d+:")
		final = re.compile(r"Final atomic structure:")
		fecha=re.compile(r"(\s*Date\s*:\s*(\d+))")
		antesF=re.compile(r"(Leaving FHI-aims\.)")
		conv=re.compile(r"(Have a nice day\.)")
		save_path = "/storage1/energy/Resultados/FHI/"
		completeName = os.path.join(save_path, "coord_"+nom)         
		c1="No convergio"
		fech=""
		fecha1=""
		
		new = open(completeName, 'w')
		new.write("#\t\t x[A]\t\t y[A]\t\t z[A]\n")
		while True:
			line = f.readline()
			if not line: break
		
			nA = n.search(line)
			word = palabra.search(line)
			aux = coord.search(line)
			end = final.search(line)
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
			if co != None:
				c1="Convergio"
		new.close()
		try:
			
			new=open(completeName, 'r').read()
			binaryF = f.read()
			cur.execute("INSERT INTO fhi(archivo,titulo,fecha,convergencia,coordenadas,path) VALUES (%s,%s,%s,%s,%s,%s)", (psycopg2.Binary(binaryF),nom,fecha1,c1,new,ruta))
			conn.commit()
			f.close()
				
		except psycopg2.DatabaseError, dbe:
			print str(dbe)
			return(None)
		except Exception, e:
			print str(e)
			return(None)
	
	
	def nalewajski(self,f,nom,ruta):
		palabra = re.compile(r"(B\sO\sN\sD\s-\sO\sR\sD\sE\sR\s*A\sN\sA\sL\sY\sS\sI\sS)")
		dista = re.compile(r"(\s*DIST.\s*\[A\]\s*BOND-ORDERS)")
		thes = re.compile(r"(\s*\(THRESHOLD\s=\s*\d.\d+\s*\))")
		total = re.compile(r"(\s*\d-CENTER\s*TOTAL\s*\(\*\))")
		form = re.compile(r"([A-Z]+\s*(\d+\s-\s[A-Z]+)\s*(\d+)\s*(\d+.\d+)\s*(\d+.\d+)\s*(\d+.\d+))")
		suma = re.compile(r"Sum\s*:\s*(\d+.\d+)\s*(\d+.\d+)")
		fecha=re.compile("(ADF\s*(\d+\.\d+)\s*RunTime:\s*(\w+\-\d+)\s*(\d+:\d+:\d+)\s*Nodes:\s*(\d+)\s*Procs:\s*(\d+))")
		conv=re.compile("(Symmetry \s*:\s*NOSYM)")
		save_path = "/storage1/energy/Resultados/ADF/"
		completeName = os.path.join(save_path, "nalewajski_"+nom)         
		new = open(completeName, 'w')
		co="No Convergio"
		fech=""
		while True:
			line = f.readline()
			if not line: break
		
			boa = palabra.search(line)
			d = dista.search(line)
			t = thes.search(line)
			centerT = total.search(line)
			end = form.search(line)
			s = suma.search(line)
			fe=fecha.search(line)
			conv1=conv.search(line)
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
			if conv1!=None:
				co="Convergio"
			
		new.close()
		try:
			new=open(completeName, 'r').read()
			binaryF = f.read()
			cur.execute("INSERT INTO adf(archivo,titulo,fecha,convergencia,nalewajski,path) VALUES (%s,%s,%s,%s,%s,%s)", (psycopg2.Binary(binaryF),nom,fech,co,new,ruta))
			conn.commit()
			f.close()	
			
		except psycopg2.DatabaseError, dbe:
			print str(dbe)
			return(None)
		except Exception, e:
			print str(e)
			return(None)
	
	def nicsG(self,f,nom,ruta):
		nics1 = re.compile(r"((\d+)\s*(Bq)\s*(Isotropic\s*=)\s*(-?\d+\.\d+)\s*(Anisotropy\s*=)\s*(-?\d+\.\d+))")		
		conv=re.compile(r"(Normal termination of Gaussian \d+ at (\w+\s+\w+\s+\d+)\s+(\d+:\d+:\d+)\s+(\d+))")
		c="No convergio"
		fecha=""
		while True:
			line = f.readline()
			if not line: break
			
			n=nics1.search(line)
			conve=conv.search(line)
			
			if n != None:
				ni=n.group(5)
				aux=float(ni)
			if conve!=None:
				c="Convergio"	
				fecha=conve.group(2)
			
		try:
				
			binaryF = f.read()
			cur.execute("INSERT INTO Gaussian(archivo,titulo,fecha,convergencia,nics,path) VALUES (%s,%s,%s,%s,%s,%s)", (psycopg2.Binary(binaryF),nom,fecha,c,aux,ruta))
			conn.commit()
			f.close()		
		except psycopg2.DatabaseError, dbe:
			print str(dbe)
			return(None)
		except Exception, e:
			print str(e)
			return(None)
	
	def mdpG(self,f,nom,ruta):
		palabra1=re.compile(r"(Molecular\sdynamics\sproduction\s:\n)")
		tiempo=re.compile("(\*\*\s*Time\s*:\s*(\d+\.\d+)\s*ps\s*:)")
		total_energy=re.compile("((Total energy\s*\(eV\))\s=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
		temperature=re.compile("((Temperature\s*\(K\))\s*=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
		pression=re.compile("((Pressure\s*\(GPa\))\s*=\s*(-?\d+\.\d+)\s*(-?\d+\.\d+))")
		fecha=re.compile("(Job Started  at\s*(\d+:\d+\.\d+)\s*(\d+\w+\s*\w+\s*\d+))")
		save_path = "/storage1/energy/Resultados/GULP/"
		completeName = os.path.join(save_path, "ext_"+nom)    
		new=open(completeName,'w')
		new.write("#Tiempo  Energia total  Temperatura  Presion\n")
		time=[]
		tener=[]
		temp=[]
		pr=[]
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
		try:
			
			new=open(completeName, 'r').read()
			binaryF = f.read()
			cur.execute("INSERT INTO gulp(archivo,titulo,fecha,datos,path) VALUES (%s,%s,%s,%s,%s)", (psycopg2.Binary(binaryF),nom,fech,new,ruta))
			conn.commit()
			f.close()
			
		except psycopg2.DatabaseError, dbe:
			print str(dbe)
			return(None)
		except Exception, e:
			print str(e)
			return(None)
		
			
	

	def clasificar(self,filename):
		adf = re.compile(r"(Amsterdam\s*Density\s*Functional)")
		gaussian = re.compile(r"(Gaussian\s*System)")
		fhi_aims = re.compile(r" (\s*FHI-aims\s*)")
		gulp = re.compile(r"(GENERAL\s*UTILITY\s*LATTICE\s*PROGRAM)")
		turbomole = re.compile(r"(TURBOMOLE)")
		f_name = os.path.basename(filename)
		nombreD = f_name.partition("/")
		nom = nombreD[0]
		path_obt=os.path.dirname(os.path.abspath(filename))
		f = open(filename)
		while True:
			line = f.readline()
			if not line: break
			
			adf1 = adf.search(line)
			gaussian1 = gaussian.search(line)
			fhi_aims1 = fhi_aims.search(line)
			gulp1 = gulp.search(line)
			turbomole1 = turbomole.search(line)
			
			if adf1 != None:
				self.nalewajski(f,nom,path_obt)
				return 0
				
			if gaussian1 != None:
				self.nicsG(f,nom,path_obt)
				return 0
				
			if fhi_aims1 != None:
				self.coordenadas(f,nom,path_obt)
				return 0
			
			if gulp1 != None:
				self.mdpG(f,nom,path_obt)
				return 0
				
			if turbomole1 != None:
				self.dipole_moment(f,nom,path_obt)
				return 0
	
	def process(self, event):
		"""
		event.event_type
		'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
		True | False
		event.src_path
		path/to/observed/file
		"""
		save_f="/storage1/energy/"
		completeName = os.path.join(save_f, "registro.out")
		reg_file=open(completeName,'a')
		reg_file.writelines("Fecha y hora: "+time.strftime("%c")+"\n")
		reg_file.writelines(event.src_path+"\n")
		reg_file.writelines(event.event_type+"\n")

		
	def on_moved(self, event):
		self.process(event)
			
	def on_modified(self, event):
		archivos2 = Queue.Queue()
		self.process(event)
		if os.path.isfile(event.src_path):
			archivos2.put(event.src_path)
			while not archivos2.empty():
				self.clasificar((archivos2.get()))
		
	def on_created(self, event):
		archivos = Queue.Queue()
		self.process(event)
		if os.path.isfile(event.src_path):
			archivos.put(event.src_path)
			while not archivos.empty():
				self.clasificar((archivos.get()))
			
		
	def on_deleted(self, event):
		self.process(event)

def main():
	path="/storage1/energy/DatosComun"
	observer = Observer()
	observer.schedule(MyHandler(), path, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(5)
	except KeyboardInterrupt:
		observer.stop()
	
	observer.join()




if __name__ == "__main__":
	main()
	
