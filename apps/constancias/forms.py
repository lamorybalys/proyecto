from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

#<-----FORM JUBILACION----->
class JubilacionForm(forms.ModelForm):
	class Meta:
		model = Jubilacion
		fields = [
			"expediente",
		]
class PensionForm(forms.ModelForm):
	class Meta:
		model = Pension
		fields = [
			"expediente",
			"motivo",
		]
class PensionUpdate(forms.ModelForm):
	class Meta:
		model = Jubilacion
		fields = [
			"estatus",
			"observacion"
		]
class RetiroForm(forms.ModelForm):
	class Meta:
		model = Cambio
		fields = [
			"expediente",
			"motivo"
		]
class JubilacionUpdate(forms.ModelForm):
	class Meta:
		model = Jubilacion
		fields = [
			"estatus",
			"observacion"
		]
class SeguroUpdate(forms.ModelForm):
	class Meta:
		model = Segu_Social
		fields = [
			"estatus",
			"observacion",
			"fech_func",
			"const_1402",
			"const_1403"
		]
class CambioUpdate(forms.ModelForm):
	class Meta:
		model = Cambio
		fields = [
			"estatus",
			"observacion"
		]

#<-----FORM DESCANSO TRIMESTRAL----->
class Descan_TrimesForm(forms.ModelForm):
	class Meta:
		model = Descan_Trimes
		fields = [
			"fech_solici",
			"fech_fin",
			"opci",
			"carg_libr_nom",
			"enfer",
			"accid",
			"falle_fami_metro",
			"falle_fami_exte",
			"nacim_hij",
			"com_ant_tribu",
			"matrim",
			"pre_natal",
			"post_natal",
			"asis_curs_confe",
			"enfer_fami",
			"estu_acade",
			"dili_pers",
			"otro",
		]
class Descan_TrimesFormUpdate(forms.ModelForm):
	class Meta:
		model = Descan_Trimes
		fields = [
			"observacion",
			"estatus",

		]

#<-----FORM VACACIONES----->
class VacacionesForm(forms.ModelForm):
	class Meta:
		model = Vacaciones
		fields = [
			"cod_vaca",
			"fech_inic",
			"fech_rein",
			"fech_culm",
			"observacion",
			"coordinacion",
			"direc_linea",
			"direc_gener",
			"exten_tele",
			"tipo_vaca",
			"periodo",
		]
	



#<-----FORM SEGURO SOCIAL----->
class Segu_SocialForm(forms.ModelForm):
	class Meta:
		model = Segu_Social
		fields = [
			"expediente",
		]

#<-----FORM CRONOLOGICO----->
class CronologicoForm(forms.ModelForm):
	class Meta:
		model = Cronologico
		fields = [
			"cod_crono",
			"fech_des",
			"fech_has",
			"carg_ante",
			"institucion",
			"expediente",
		]
class VacacionesUpdate(forms.ModelForm):
	class Meta:
		model = Vacaciones
		fields = [
			"observacion",
			"coordinacion",
			"direc_linea",
			"direc_gener",
			"exten_tele",
			"estatus",
		]


#<-----FORM EVALUACION----->
class EvaluacionForm(forms.ModelForm):
	class Meta:
		model = Evaluacion
		fields = [
			"cod_evalua",
			"periodo",
			"año",
			"escala",
			"nota",
			"expediente",
		]

class VacaFormArc(forms.ModelForm):
	class Meta:
		model = Vacaciones
		fields ='__all__'

class PeriodoForm(forms.ModelForm):
	class Meta:
		model = Periodo
		fields ='__all__'

class JubiiForm(forms.ModelForm):
	class Meta:
		model = Jubilacion
		fields ='__all__'

class SeguroForm(forms.ModelForm):
	class Meta:
		model = Segu_Social
		fields ='__all__'