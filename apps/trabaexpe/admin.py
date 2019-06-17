# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class AdminTrabajador(admin.ModelAdmin):
	list_display = ["cedu_trab","nomb_trab","ape_trab", 
					"cod_tele","telefono","sexo", 
					"num_ric","cod_rac","fech_ing_pub", 
					"fech_ing_inst","fech_naci",
					"cargos", "estat_traba",]

admin.site.register(Trabajador, AdminTrabajador)

class AdminDirectores(admin.ModelAdmin):
	list_display = ["cedu_direc","nomb_direc","apel_direc","carg_direc"]

admin.site.register(Directores, AdminDirectores)

class AdminExpedientes(admin.ModelAdmin):
	list_display = ["trabajador","titulo","estado_civil","cart_cunc","act_matr",
					"act_divor","act_difu","cop_cedula",
					"parti_nacimiento","regi_cen_per","sinte_curri",
					"fideicomiso","recibo_pago","directores"]

admin.site.register(Expedientes, AdminExpedientes)

class AdminSueldo(admin.ModelAdmin):
	list_display = ["expediente",
"sueldo",
"compensasion",
"profesionalizacion",
"antiguedad"]

admin.site.register(Sueldo, AdminSueldo)