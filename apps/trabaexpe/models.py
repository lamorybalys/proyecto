from django.db import models
from apps.constancias.models import *
from seguridad.models import User
from datetime import datetime

class Trabajador(models.Model):
	cargo = (
		("Empleado (a) ","Empleado (a)"),
		("Medico (a) ","Medico (a)"),
		("Obrero (a) ","Obrero (a)"),
	)
	codigo=(
		("0424","0424"),
		("0414","0414"),
		("0426","0426"),
		("0416","0416"),
		("0412","0412"),
		("0257","0257"),
	)
	sexo=(
		("Femenino","Femenino"),
		("Masculino","Masculino"),
	)
	
	estatus=(
		("Fijo","Fijo"),
		("Contratado","Contratado"),
	)
	
	gra=(
		("","Seleccione"),
		("1","1"),
		("2","2"),
		("3","3"),
		("4","4"),
		("5","5"),
		("6","6"),
		("7","7"),
		("8","8"),
		("9","9"),
		("10","10"),
		("11","11"),
		("12","12"),
	)
	emp = (
		("","Seleccione"),
		('ENFERMERA (o) I','ENFERMERA (o) I'),
		
		('ASISTENTE DE RAYOS X','ASISTENTE DE RAYOS X'),

		('ASISTENTE ADMINISTRATIVO I','ASISTENTE ADMINISTRATIVO I'),

		('INTENDENTE DE HOSPITAL III','INTENDENTE DE HOSPITAL III'),

		('ENFERMERA II','ENFERMERA II'),

		('INGENIERO MECANICO I','INGENIERO MECANICO I'),

		('ADMINISTRADOR I','ADMINISTRADOR I'),

		('CAPELLAN','CAPELLAN'),

		('ASISTENTE DE LABORATORIO CLINICO I','ASISTENTE DE LABORATORIO CLINICO I'),

		('ASISTENTE ADMINISTRATIVO III','ASISTENTE ADMINISTRATIVO III'),

		('CONTABILISTA I','CONTABILISTA I'),

		('TRABAJADOR SOCIAL I','TRABAJADOR SOCIAL I'),

		('ASISTENTE DE ANALISTA III','ASISTENTE DE ANALISTA III'),

		('ASISTENTE DE DIETETICA','ASISTENTE DE DIETETICA'),

		('CONTABILISTA II TECNICO','CONTABILISTA II TECNICO'),
		
		('RADIOLOGO I','RADIOLOGO I'),

		('TECNICO DE REGISTRO Y EST. DE SALUD I','TECNICO DE REGISTRO Y EST. DE SALUD I'),

		('ANALISTA DE PERSONAL III','ANALISTA DE PERSONAL III'),

		('DIETISTA I ENFERMERA(O)','DIETISTA I ENFERMERA(O)'),

		('ESPECIALISTA I','ESPECIALISTA I'),

		('TECNICO DE REGISTRO Y EST. DE SALUD II','TECNICO DE REGISTRO Y EST. DE SALUD II'),

		('SOCIOLOGO I TECNICO HISTOLOGO','SOCIOLOGO I TECNICO HISTOLOGO'),

		('ENFERMERA(O) ESPECIALISTA II','ENFERMERA(O) ESPECIALISTA II'),

		('SECRETARIO I','SECRETARIO I'),

		('CONTADOR I','CONTADOR I'),

		('SUPERVISOR DE SERVICIOS GENERALES I','SUPERVISOR DE SERVICIOS GENERALES I'),

		('FARMACEUTICO II','FARMACEUTICO II'),

		('ASISTENTE ADMINISTRATIVO IV','ASISTENTE ADMINISTRATIVO IV'),

		('ASISTENTE DE TERAPIA','ASISTENTE DE TERAPIA'),

		('ARCHIVISTA I','ARCHIVISTA I'),

		('OPERADOR DE EQUIPO DE COMPUTACION I','OPERADOR DE EQUIPO DE COMPUTACION I'),

		('PLANIFICADOR I','PLANIFICADOR I'),

		('TECNICO EQUIPO MEDICO I','TECNICO EQUIPO MEDICO I'),

		('INGENIERO ELECTRICISTA I','INGENIERO ELECTRICISTA I'),

		('EQUIPO DE COMPUTACION II','EQUIPO DE COMPUTACION II'),

		('ANALISTA DE PROCESAMIENTO DE DATOS I','ANALISTA DE PROCESAMIENTO DE DATOS I'),

		('TECNICO RADIOLOGO II','TECNICO RADIOLOGO II'),

		('ASISTENTE DE SERVICIO SOCIAL','ASISTENTE DE SERVICIO SOCIAL'),

		('OPERADOR DE EQUIPO DE COMPUTACION III','OPERADOR DE EQUIPO DE COMPUTACION III'),

		('BIOANALISTA II','BIOANALISTA II'),

		('ANALISTA DE PERSONAL I','ANALISTA DE PERSONAL I'),

		('PSICOLOGO I ','PSICOLOGO I '),
		
		('ASISTENTE DE OFICINA I','ASISTENTE DE OFICINA I'),

		('BIOANALISTA I','BIOANALISTA I'),

		('ANALISTA DE PERSONAL II','ANALISTA DE PERSONAL II'),

		('FISIOTERAPISTA II','FISIOTERAPISTA II'), 
		
		('PROGRAMADOR II','PROGRAMADOR II'),

		('ALMACENISTA I','ALMACENISTA I'),

		('ASISTENTE DE FARMACIA I','ASISTENTE DE FARMACIA I'),

		('FISIOTERAPISTA I','FISIOTERAPISTA I'),
		
		('ASISTENTE DE ANALISTA II','ASISTENTE DE ANALISTA II'),
		
		('ODONTOLOGO I','ODONTOLOGO I'),

		('HIGIENISTA DENTAL I','HIGIENISTA DENTAL I'),

		('ASISTENTE DE ESTADISTICA I','ASISTENTE DE ESTADISTICA I'),

		('ANALISTA DE ORGANIZACIÓN Y SISTEMAS I','ANALISTA DE ORGANIZACIÓN Y SISTEMAS I'),

		('SUPERVISOR DE SERVICIOS GENERALES II','SUPERVISOR DE SERVICIOS GENERALES II'),

		('TERAPEUTA OCUPACIONAL II','TERAPEUTA OCUPACIONAL II'),

		('ASISTENTE DE SALUD PUBLICA','ASISTENTE DE SALUD PUBLICA')
	)
	obr = (
		("","Seleccione"),
		('CAMARERA','CAMARERA'), 
		('CAMILLERO','CAMILLERO'), 
		('AUXILIAR DE LABORATORIO','AUXILIAR DE LABORATORIO'),
		('COSTURERA','COSTURERA'),
		('AUXILIAR SERV.OFICINA','AUXILIAR SERV.OFICINA'),
		('MENSAJERO','MENSAJERO'),
		('MENSAJERO-MOTORIZADO','MENSAJERO-MOTORIZADO'),
		('AUXILIAR DEENFERMERÍA','AUXILIAR DEENFERMERÍA'),
		('ASEADOR','ASEADOR'), 
		('PORTERO','PORTERO'), 
		('AUXILIAR DE TERAPIA','AUXILIAR DE TERAPIA'),
		('ASCENSORISTA','ASCENSORISTA'),
		('RECOLECTOR DESECHOS SOLIDOS','RECOLECTOR DESECHOS SOLIDOS'),
		('LENCERO','LENCERO'),
		('SUPERVISOR DE SERV. INTER','SUPERVISOR DE SERV. INTER'),
		('AYUDANTE DE SERVICIOS DE COCINA','AYUDANTE DE SERVICIOS DE COCINA'),
		('LAVANDERO','LAVANDERO'), 
		('RECEPTOR','RECEPTOR'), 
		('INFORMADOR','INFORMADOR'),
		('CARPINTERO','CARPINTERO'), 
		('ELECTROMECANICO','ELECTROMECANICO'),
		('AUXILIAR DE FARMACIA','AUXILIAR DE FARMACIA'),
		('VIGILANTE','VIGILANTE'),
		('ALBAÑIL','ALBAÑIL'),
		('AYUDANTE DE ALMACEN','AYUDANTE DE ALMACEN'),
		('SUPERVISOR DE PLANTA HIDROELÉCTRICA','SUPERVISOR DE PLANTA HIDROELÉCTRICA'),
		('CHOFER','CHOFER '),
		('AYUDANTE','AYUDANTE'),
		('SERVICIOS GENERALES','SERVICIOS GENERALES'),
		('AUXILIAR DE RAYOS X','AUXILIAR DE RAYOS X'),
		('NIÑERA','NIÑERA'),
		('JARDINERO','JARDINERO'),
		('DESPENSERO','DESPENSERO'),
		('MECÁNICO DE REFRIGERACIÓN','MECÁNICO DE REFRIGERACIÓN'),
		('OPERARIO DE MÁQUINA LIVIANA','OPERARIO DE MÁQUINA LIVIANA'),
		('PINTOR','PINTOR '),
		('MECANICO AUTOMOTRIZ','MECANICO AUTOMOTRIZ'),
		('AUXILIAR DE AUTOPSIA','AUXILIAR DE AUTOPSIA'),
		('PLOMERO OPERAD. MAQ. FOTOCOP.','PLOMERO OPERAD. MAQ. FOTOCOP.'),
		('HERRERO','HERRERO'),
		('COCINERO','COCINERO'),
		('SUPERVISOR SERVICIOS ESPECIALES','SUPERVISOR SERVICIOS ESPECIALES'),
	)
	cedu_trab = models.IntegerField(unique=True, blank=True)
	nomb_trab = models.CharField(max_length=30)
	ape_trab = models.CharField(max_length=30)
	cod_tele = models.CharField(max_length=20,choices=codigo)
	grado = models.CharField(max_length=20,choices=gra,blank=True,null=True,default="1")
	empleados = models.CharField(max_length=200,choices=emp,blank=True,null=True)
	obreros = models.CharField(max_length=200,choices=obr,blank=True,null=True)
	telefono = models.CharField(max_length=200,null=True)
	sexo = models.CharField(max_length=50, choices=sexo)
	num_ric = models.CharField(max_length=200)
	cod_rac = models.CharField(max_length=200,blank=True)
	fech_ing_pub = models.DateField(max_length=30)
	fech_ing_inst = models.DateField(max_length=30)
	fech_naci = models.DateField(max_length=30)
	
	cargos = models.CharField(max_length=50, choices=cargo)
	estat_traba = models.CharField(max_length=50, choices=estatus)
	usuario = models.ForeignKey(User, blank=True,null=True)

	def nombre_completo(self):
		full_name = '%s %s' % (self.nomb_trab, self.ape_trab)
		return full_name.strip().upper()
	
	def antiguedad(self):
		return int((datetime.now().date() - self.fech_ing_inst).days / 365.25)
	
	def edad(self):
		return int((datetime.now().date() - self.fech_naci).days / 365.25)

	def __str__(self):
		return '%s - %s %s %s' %(self.cedu_trab,self.nomb_trab,self.ape_trab,self.cargos)

class Directores(models.Model):
	carg = (
		("Director (a) Hospital Miguel Oraa", 
		 "Director (a) Hospital Miguel Oraa"),
		
		("Director (a) Recursos Humanos Hospital Miguel Oraa", 
		 "Director (a) Recursos Humanos Hospital Miguel Oraa"),
		
		("Director (a) Region", "Director (a) Region"),
		("Director (a) Recursos Humanos Region ", 
		 "Director (a) Recursos Humanos Region"),

		("Archivera (o)", "Archivera (o)"),
	)
	cedu_direc = models.IntegerField(unique=True)
	nomb_direc = models.CharField(max_length=30)
	apel_direc = models.CharField(max_length=30)
	carg_direc = models.CharField(max_length=50,choices=carg , null=True,blank=True)
	
	def __str__(self):
		return '%s - %s %s %s' %(self.cedu_direc,self.nomb_direc,self.apel_direc,self.carg_direc)

class Expedientes(models.Model):
	est_civil = (
		("Soltero (a)", "Soltero (a)"),
		("Casado (a)", "Casado (a)"),
		("Divorsiado (a)", "Divorsiado (a)"),
		("Viudo (a)", "Viudo (a)"),
	)
	titulo = models.BooleanField()
	estado_civil = models.CharField(max_length=30, choices=est_civil)
	cart_cunc = models.BooleanField(blank=True)
	act_matr = models.BooleanField(blank=True)
	act_divor = models.BooleanField(blank=True)
	act_difu = models.BooleanField(blank=True)
	cop_cedula = models.BooleanField()
	parti_nacimiento = models.BooleanField()
	regi_cen_per = models.BooleanField()
	sinte_curri = models.BooleanField()
	fideicomiso = models.BooleanField()
	recibo_pago = models.BooleanField()
	trabajador = models.OneToOneField(Trabajador)
	directores = models.ForeignKey(Directores, blank=True)


	def __str__(self):
		return '%s - %s %s' %(self.trabajador.cedu_trab, self.trabajador.nomb_trab,self.trabajador.ape_trab)
	
	def vacaciones(self):
		return int((datetime.now().date() - self.trabajador.fech_ing_inst).days / 365.25)

class Sueldo(models.Model):
	expediente= models.ForeignKey(Expedientes)
	sueldo = models.CharField(max_length=200)
	compensasion = models.CharField(max_length=200)
	profesionalizacion = models.CharField(max_length=200)
	antiguedad = models.CharField(max_length=200)

	def __str__(self):
		return 'Sueldo de {},'.format(self.expediente.trabajador.nomb_trab)