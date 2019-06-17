from django.conf.urls import url
from .views import *
from . import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
	#<----- Seguro Social ----->
	url(r'^ley/$', login_required(LeyPDF), name="ley"),
	url(r'^trabajo/$', login_required(TrabajoPDF), name="trabajo"),
	url(r'^trabajosueldo/$', login_required(TrabajoSueldoPDF), name="trabajoSueldo"),
	url(r'^vacacionesdetail/(?P<pk>[0-9]+)/$', login_required(VacaDetailPDF), name="vacadetail"),
	url(r'^decadetail/(?P<pk>[0-9]+)/$', login_required(DecaDetailPDF), name="decadetail"),
	url(r'^descanso/$', login_required(DescansoPDF), name="descanso"),
	url(r'^vacaciones/$', login_required(VacacionesPDF), name="vacaciones"),
	url(r'^trabajadores/$', login_required(TrabajadoresPDF), name="trabajadores"),
	url(r'^cambio/$', login_required(CambioPDF), name="cambio"),
	url(r'^jubilacion/$', login_required(JubPDF), name="jubilacion"),
	url(r'^pension/$', login_required(PenPDF), name="pension"),
	url(r'^seguro/$', login_required(SegPDF), name="seguro"),
	
]