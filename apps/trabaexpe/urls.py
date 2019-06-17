from django.conf.urls import url
from .views import *
from . import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^upd_noti/$', NotificacionUpdate.as_view(), name="updNoti"),
	url(r"^admin/$", login_required(PanelAdministrativo), name="Admin"),
	#<----- Trabajador ----->
	url(r'^agg/$', AggWorker, name="Aggm"),
	url(r'^listworker/$', login_required(ListTrabajador), name="Listworker"),
	url(r'^ver_worker/(?P<pk>[0-9]+)/$', login_required(VerTrabajador), name="verWorker"),
	#<----- ----->

	#<----- Director ----->
	url(r'^aggdire/$', login_required(AggDirectores), name="Aggdire"),
	url(r'^listdire/$', login_required(ListDirectores), name="ListDirectores"),
	url(r'^editdire/(?P<pk>[0-9]+)/edit/$', editarDirectores, name='editar'),
	url(r'^ver_direct/(?P<pk>[0-9]+)/$', login_required(VerDirectores), name="verDirect"),
	#<----- ----->

	#<----- Expediente ----->
	url(r'^aggexpe/$', aggExpedientes, name="Aggexpe"),
	url(r'^listexpe/$', login_required(ListExpediente), name="Listexpe"),
	url(r'^ver_expe/(?P<pk>[0-9]+)/$', login_required(VerExpediente), name="verExpe"),
	#<----- ----->

	#<----- Expediente ----->
	url(r'^trabajador_pdf(?P<pk>[0-9]+)/$', trabajador_pdf, name='trabajador_pdf'),

	#<-----Sueldo ----->
	url(r'^aggsueldo/$', aggesueldo, name="sueldo"),

	#<----- Mensaje ----->
	url(r'^mensaje/$', Mensaje, name="mensaje"),

	#<----- Solicitud Vacaciones ----->
	url(r'^solivaca/$', SoliVaca, name="AlertVaca"),
	
]