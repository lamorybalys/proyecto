from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

# class UsuarioForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     email = forms.CharField(max_length=30, required=True)

#     class Meta:
#         model = User
#         fields = ("email", "first_name", "last_name", "password1", "password2")


class TrabajadorForm(forms.ModelForm):
	class Meta:
		model = Trabajador
		fields = [
			"cedu_trab", 
			"nomb_trab",
			"ape_trab", 
			"cod_tele",
			"telefono", 
			"sexo", 
			"num_ric", 
			"cod_rac", 
			"fech_ing_pub", 
			"fech_ing_inst",
			"fech_naci",
			"cargos",
			"obreros",
			"empleados",
			"estat_traba",
		]

class ExpedientesForm(forms.ModelForm):
	class Meta:
		model = Expedientes
		fields = [
			"titulo",
			"estado_civil",
			"cart_cunc",
			"act_matr",
			"act_divor",
			"act_difu",
			"cop_cedula",
			"parti_nacimiento",
			"regi_cen_per",
			"sinte_curri",
			"fideicomiso",
			"recibo_pago",
			"trabajador",
			"directores",

		]
	def __init__(self, *args, **kwargs):
		super(ExpedientesForm, self).__init__(*args, **kwargs)
		expedientes = Expedientes.objects.all().values_list('trabajador')
		trabajador = Trabajador.objects.all().exclude(pk__in=expedientes)

		self.fields['trabajador'].queryset = trabajador
		#self.fields['expediente'].queryset = Expediente.objects.filter(estatu="1")
			
class DirectoresForm(forms.ModelForm):
	class Meta:
		model = Directores
		fields = [
			"cedu_direc",
			"nomb_direc",
			"apel_direc",
			"carg_direc",
		]