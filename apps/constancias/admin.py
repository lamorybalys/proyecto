# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

#<-----DESCANSO TRIMESTRAL----->
class AdminDescan_Trimes(admin.ModelAdmin):
	list_display = ["cod_des_tri","fech_solici","fech_fin","observacion","estatus","expediente"]

admin.site.register(Descan_Trimes, AdminDescan_Trimes)

class AdminCambio(admin.ModelAdmin):
	list_display = ["expediente","estatus"]

admin.site.register(Cambio, AdminCambio)
#<-----VACACIONES----->
class AdminVacaciones(admin.ModelAdmin):
	list_display = ["cod_vaca",
					"fech_inic","fech_culm","observacion","coordinacion",
					"direc_linea","direc_gener","exten_tele","tipo_vaca",
					"periodo"]

admin.site.register(Vacaciones, AdminVacaciones)

class AdminPeriodo(admin.ModelAdmin):
	list_display = ["expediente",
					"periodo","dias","estatus"]

admin.site.register(Periodo, AdminPeriodo)

#<-----JUBILACION----->
class AdminJubilacion(admin.ModelAdmin):
	list_display = ["cod_jubila","expediente"]

admin.site.register(Jubilacion, AdminJubilacion)

#<-----SEGURO SOCIAL----->
class AdminSegu_Social(admin.ModelAdmin):
	list_display = ["cod_seg_soc","fech_func","const_1402",
					"const_1403","expediente"]

admin.site.register(Segu_Social, AdminSegu_Social)
class AdminPension(admin.ModelAdmin):
	list_display = ["observacion",
"motivo",
"estatus",
"fecha_s",
"cod_pen",
"expediente"]

admin.site.register(Pension, AdminPension)

#<-----CRONOLOGICO----->
class AdminCronologico(admin.ModelAdmin):
	list_display = ["cod_crono","fech_des","fech_has","carg_ante","institucion","expediente"]

admin.site.register(Cronologico, AdminCronologico)

#<-----EVALUACION----->
class AdminEvaluacion(admin.ModelAdmin):
	list_display = ["cod_evalua","periodo","año","escala","nota","expediente"]

admin.site.register(Evaluacion, AdminEvaluacion)