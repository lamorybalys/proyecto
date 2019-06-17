from django.conf.urls import url
from .views import *
from . import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
	#<----- Seguro Social ----->
	url(r'^listnoti/$',login_required(ListNoti), name="Listnoti"),

	url(r'^aggseg/$', login_required(AggSegSoci), name="Aggseg"),
	url(r'^listseg/$', login_required(ListSegSoci), name="Listseg"),
	url(r'^ver_segsoc/(?P<pk>[0-9]+)/$', login_required(VerSegSoci), name="verSegSoc"),
	url(r'^upd_segsoc/(?P<pk>[0-9]+)/$', login_required(EditarSegSoci), name="updSegSoc"),

	#<-----  ----->

	#<----- Cronologico ----->
	url(r'^crono/$',login_required(AggCronologico), name="Aggcrono"),
	url(r'^listcrono/$',login_required(ListCrono), name="Listcrono"),
	url(r'^ver_crono/(?P<pk>[0-9]+)/$', login_required(VerCrono), name="verCrono"),
	#<-----  ----->

	#<----- Vacaciones ----->
	url(r'^vaca/$',login_required(AggVacaciones), name="Aggvaca"),
	url(r'^periodo/$',login_required(periodo), name="periodo"),

	url(r'^listvaca/$',login_required(ListVaca), name="Listvaca"),
	url(r'^ver_vaca/(?P<pk>[0-9]+)/$', login_required(VerVaca), name="verVaca"),
	url(r'^editvaca/(?P<pk>[0-9]+)/edit/$', login_required(EditarVaca), name='editVaca'),
	url(r'^estatus/(?P<pk>[0-9]+)$', RecibirVacaciones, name="estatus"),
	url(r'^(?P<pk>\d+)/espera/$', EsperaVacaciones, name="espera"),
	#<-----  ----->

	#<----- Jubilacion ----->
	url(r'^jubi/$',login_required(AggJubilacion), name="Aggjubi"),
	url(r'^listjubi/$',login_required(ListJubi), name="Listjubi"),
	url(r'^ver_jubi/(?P<pk>[0-9]+)/$', login_required(VerJubi), name="verJubi"),
	url(r'^upd_jubi/(?P<pk>[0-9]+)/$', login_required(EditarJubi), name="updJubi"),
	
	#<----- Pension ----->
	url(r'^pens/$',login_required(AggPension), name="Aggpen"),
	url(r'^listpen/$',login_required(ListPen), name="Listpen"),
	url(r'^ver_pen/(?P<pk>[0-9]+)/$', login_required(VerPen), name="verPen"),
	url(r'^upd_pen/(?P<pk>[0-9]+)/$', login_required(EditarPen), name="updPen"),




	#<----- CAMBIO DE INSTITUCION ----->
	url(r'^cambio/$',login_required(AggRetiro), name="AggRetiro"),
	url(r'^listreti/$',login_required(ListReti), name="Listreti"),
	url(r'^upd_reti/(?P<pk>[0-9]+)/$', login_required(EditarReti), name="updReti"),
	url(r'^ver_reti/(?P<pk>[0-9]+)/$', login_required(VerReti), name="verreti"),

	#<----- DESCANSO/TRIMESTRAL ----->
	url(r'^des_trim/$',login_required(AggDescan_Trimes), name="Aggdes_trim"),
	url(r'^listdes_trim/$',login_required(ListDescan_Trimes), name="Listdes_trim"),
	url(r'^ver_des/(?P<pk>[0-9]+)/$', login_required(VerDescan_Trimes), name="verDes"),
	#<-----  ----->

	#<----- EVALUACION ----->
	url(r'^eva/$',login_required(AggEvaluacion), name="Aggeva"),
	url(r'^listeva/$',login_required(ListEvaluacion), name="Listeva"),
	url(r'^ver_eva/(?P<pk>[0-9]+)/$', login_required(VerEvaluacion), name="verEva"),
	#<-----  ----->
	
	#<----- Reportes Generales ----->
	# url(r'^trabajadores/$',login_required(TrabajadoresPDF), name="TrabaPDF"),
	#<-----  ----->
	#<----- Reportes Individuales ----->
	#url(r'^reporte_personas_pdf/(?P<pk>[0-9]+)/$',login_required(ReportePersonasPDF.as_view()), name="ReportePDF"),

	url(r'^reporte_personas_pdf/$',login_required(ReportePersonasPDF.as_view()), name="reporte_personas_pdf"),
	url(r'^mensaje/$', Mensaje, name="mensaje"),

	#-------Archivista------------->
	url(r'^arcvaca/$',login_required(VacacionesView), name="Aggvacaarc"),
	url(r'^arcperiodo/$',login_required(PeriodoView), name="Aggperiodo"),
	url(r'^arcjubilacion/$',login_required(JubilacionView), name="Aggjubilacion"),
	url(r'^arcseguro/$',login_required(SeguroView), name="Aggseguro"),


]