from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.trabaexpe.models import *

#<-----MODELOS DESCANSO TRIMESTRAL----->
class Descan_Trimes(models.Model):
	opcion = (
		("SOLICITUD DE PERMISO ", "SOLICITUD DE PERMISO "),
		("NOTIFICACIÓN DE INASISTENCIA ", "NOTIFICACIÓN DE INASISTENCIA "),
	)
	cod_des_tri = models.IntegerField(null=True, blank=True)
	fech_solici = models.DateField(null=True,blank=True)
	fech_fin = models.DateField(null=True,blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	opci = models.CharField(max_length=50,choices=opcion)
	carg_libr_nom = models.CharField(max_length=50, null=True, blank=True)
	enfer = models.CharField(max_length=50, null=True, blank=True)
	accid = models.CharField(max_length=50, null=True, blank=True)
	falle_fami_metro = models.CharField(max_length=50, null=True, blank=True)
	falle_fami_exte = models.CharField(max_length=50, null=True, blank=True)
	nacim_hij = models.CharField(max_length=50, null=True, blank=True)
	com_ant_tribu = models.CharField(max_length=50, null=True, blank=True)
	matrim = models.CharField(max_length=50, null=True, blank=True)
	pre_natal = models.CharField(max_length=50, null=True, blank=True)
	post_natal = models.CharField(max_length=50, null=True, blank=True)
	asis_curs_confe = models.CharField(max_length=50, null=True, blank=True)
	enfer_fami = models.CharField(max_length=50, null=True, blank=True)
	estu_acade = models.CharField(max_length=50, null=True, blank=True)
	dili_pers = models.CharField(max_length=50, null=True, blank=True)
	otro = models.CharField(max_length=150, null=True, blank=True)
	observacion = models.CharField(max_length=255,null=True, blank=True)
	est = (
		("Pendiente", "Pendiente"),
		("Aprobada", "Aprobada"),
		("Rechazada", "Rechazada"),
	)
	estatus = models.CharField(max_length=50, choices=est,null=True,blank=True,default="Pendiente")
	
	expediente = models.ForeignKey(Expedientes,blank=True,null=True,on_delete=models.CASCADE)

	def __str__(self):
		return '%s - %s ' %(self.cod_des_tri,self.expediente)

class Periodo(models.Model):
	expediente = models.ForeignKey(Expedientes,on_delete=models.CASCADE, null=True,blank=True)
	periodo = models.DateField()
	estatus = models.BooleanField(default=False)
	adelanto = models.BooleanField()
	dias = models.IntegerField()

	class Meta:
		ordering = ['-id']
	def __str__(self):
		fecha = str(int(str(self.periodo).split('-')[0])-1)+'-'+str(self.periodo).split('-')[0]

		return '{} {}, {} dias'.format(fecha,self.expediente,self.dias)

#<-----MODELOS DE VACACIONES----->
class Vacaciones(models.Model):
	tipo = (
		("Reglamentarias", "Reglamentarias"),
		("Atrasadas", "Atrasadas"),
		("Adelantadas", "Adelantadas"),
	)
	est = (
		("Pendiente", "Pendiente"),
		("Aprobada", "Aprobada"),
		("Rechazada", "Rechazada"),
	)
	cod_vaca = models.IntegerField(null=True,blank=True)
	fech_inic = models.DateField(max_length=50,null=True,blank=True)
	fech_culm = models.DateField(max_length=50,null=True,blank=True)
	fech_rein = models.DateField(max_length=50,null=True,blank=True)
	observacion = models.CharField(null=True, blank=True,max_length=255)
	coordinacion = models.CharField(max_length=255,null=True,blank=True)
	direc_linea = models.CharField(max_length=255,null=True,blank=True)
	direc_gener = models.CharField(max_length=255, null=True,blank=True)
	exten_tele = models.CharField(blank=True,null=True,max_length=255)
	tipo_vaca = models.CharField(max_length=50, choices=tipo,null=True,blank=True)
	estatus = models.CharField(max_length=50, choices=est,null=True,blank=True,default="Pendiente")
	periodo = models.ForeignKey(Periodo,on_delete=models.CASCADE)
	def __str__(self):
		return '%s - %s' %(self.cod_vaca,self.periodo.expediente)

#<-----MODELOS SEGURO SOCIAL----->
class Segu_Social(models.Model):
	est = (
		("Pendiente", "Pendiente"),
		("Procesando", "Procesando"),
		("Aprobada", "Aprobada"),
		("Rechazada", "Rechazada"),
	)
	
	estatus_seg = (
		("Egreso","Egreso"),
		("Ingreso", "Ingreso"),
		("Reingreso", "Reingreso"),
	)	
	estatus = models.CharField(max_length=50, choices=est,null=True,blank=True,default="Pendiente")
	observacion = models.CharField(null=True, blank=True,max_length=255)

	cod_seg_soc = models.IntegerField(null=True, blank=True)
	esta_seg_soc = models.CharField(max_length=20,choices=estatus_seg,default="Ingreso")
	fech_func = models.DateField(null=True, blank=True)
	const_1402 = models.BooleanField(default=False)
	const_1403 = models.BooleanField(default=False)
	expediente = models.OneToOneField(Expedientes,on_delete=models.CASCADE)

	def __str__(self):
		return '%s - %s' %(self.cod_seg_soc,self.expediente)

class Pension(models.Model):

	est = (
		("Pendiente", "Pendiente"),
		("Procesando", "Procesando"),
		("Aprobada", "Aprobada"),
		("Rechazada", "Rechazada"),
	)
	
	observacion = models.CharField(null=True, blank=True,max_length=255)
	motivo = models.CharField(null=True, blank=True,max_length=255)
	estatus = models.CharField(max_length=50, choices=est,null=True,blank=True,default="Pendiente")
	fecha_s = models.DateTimeField(auto_now_add=True)

	cod_pen = models.IntegerField(null=True, blank=True)

	expediente = models.ForeignKey(Expedientes,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.expediente)

#<-----MODELOS CRONOLOGICOS----->
class Cronologico(models.Model):
	cod_crono = models.IntegerField(null=True, blank=True)
	fech_des = models.CharField(max_length=40)
	fech_has = models.CharField(max_length=40)
	carg_ante = models.CharField(max_length=40)
	institucion = models.CharField(max_length=40)
	expediente = models.ForeignKey(Expedientes,on_delete=models.CASCADE)

	def __str__(self):
		return '%s - %s' %(self.cod_crono,self.expediente)

#<-----MODELOS EVALUACION----->
class Evaluacion(models.Model):
	cod_evalua = models.IntegerField(null=True, blank=True)
	periodo = models.CharField(max_length=40)
	año = models.CharField(max_length=40)
	escala = models.CharField(max_length=40)
	nota = models.IntegerField()
	expediente = models.ForeignKey(Expedientes,on_delete=models.CASCADE)

	def __str__(self):
		return '%s - %s' %(self.cod_evalua,self.expediente)

#<-----MODELOS DE JUBILACION----->
class Jubilacion(models.Model):
	est = (
		("Pendiente", "Pendiente"),
		("Procesando", "Procesando"),
		("Aprobada", "Aprobada"),
		("Rechazada", "Rechazada"),
	)
	observacion = models.CharField(null=True, blank=True,max_length=255)

	estatus = models.CharField(max_length=50, choices=est,null=True,blank=True,default="Pendiente")
	fecha_s = models.DateTimeField(auto_now_add=True)

	cod_jubila = models.IntegerField(null=True, blank=True)

	expediente = models.ForeignKey(Expedientes,on_delete=models.CASCADE)

	def __str__(self):
		return '%s - %s' %(self.cod_jubila,self.expediente)

class Cambio(models.Model):
	est = (
		("Pendiente", "Pendiente"),
		("Aprobada", "Aprobada"),
		("Rechazada", "Rechazada"),
	)
	estatus = models.CharField(max_length=50, choices=est,null=True,blank=True,default="Pendiente")

	motivo = models.CharField(null=True, blank=True,max_length=255)
	observacion = models.CharField(null=True, blank=True,max_length=255)
	expediente = models.OneToOneField(Expedientes,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.expediente)
	