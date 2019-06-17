from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Q
from django.conf import settings
from django.views.generic import View
from io import BytesIO
from reportlab.platypus.tables import Table, TableStyle, CellStyle, LongTable
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.platypus.tables import Table, TableStyle, CellStyle, LongTable
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle,PageBreak
from reportlab.lib.pagesizes import letter, A4,  LETTER, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, BaseDocTemplate, Frame, PageTemplate, Image, TableStyle, Spacer
import time
import datetime 
from django.utils import timezone
from datetime import datetime
from reportlab.lib.units import inch
import os
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from django.contrib.auth.models import User
from datetime import date, time

from .forms import *
from .models import *
from apps.trabaexpe.models import *
from apps.trabaexpe.forms import *
from django.contrib import messages
from django.http import JsonResponse
from seguridad.models import Notificacion
import time
from django.views.generic import CreateView, TemplateView, View 


def ListNoti(request):
	if request.user.is_trabajador:
		notifications = Notificacion.objects.filter(tipo="trabajador",usuario=request.user).order_by('-fecha')
	elif request.user.is_analista_social:
		notifications = Notificacion.objects.filter(tipo="seguro").order_by('-fecha')
	elif request.user.is_analista_jubilacion:
		notifications = Notificacion.objects.filter(tipo="jubilacion").order_by('-fecha')
	elif request.user.is_analista_vacaciones:
		notifications = Notificacion.objects.filter(tipo="vacaciones").order_by('-fecha')
	context = {'notifications':notifications}
	return render(request,'panel/ListNoti.html', context)

# <-----SEGURO SOCIAL----->
def AggSegSoci(request):
	trabajador = Trabajador.objects.get(usuario=request.user)
	expediente = Expedientes.objects.get(trabajador=trabajador)

	if request.user.is_staff:
		if request.method == 'POST':
			form = Segu_SocialForm(request.POST)
			if form.is_valid():
				fom = form.save()
				fecha = datetime.now().strftime('%d%m%Y')
				codigo = str(fecha)+str(fom.pk)
				Segu_Social.objects.filter(expediente=expediente).update(cod_seg_soc=codigo)
				Notificacion(
					usuario=trabajador.usuario,
					contenido="El trabajador {} ha solicitado que lo registren en el seguro social".format(trabajador.nomb_trab),
					tipo="seguro",
					url="/constancias/ver_segsoc/"+str(fom.pk)
					).save()

			else:
				return render(request, "panel/seguro_social/aggSeg.html", {"segu_social":form})
			messages.add_message(request, messages.INFO, "Solicitud registrada con éxito.")
			return redirect('Constancias:Aggseg')

		else:
			form = Segu_SocialForm()
			seguro =  Segu_Social.objects.filter(expediente=expediente).exclude(estatus='Rechazada')
			if seguro.exists():
				seguro = seguro.first()
			else:
				seguro = False
		return render(request,'panel/seguro_social/aggSeg.html',{"expediente":expediente,'segu_social':form,"seguro":seguro})
	else:
		return render(request, "restringido.html", {})

def ListSegSoci(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		segu_social = Segu_Social.objects.filter(expediente=expediente).order_by('id')
	else:
		segu_social = Segu_Social.objects.all()
	context = {'segu_social':segu_social}
	return render(request,'panel/seguro_social/ListSegu_Social.html', context)

# <-----VER----->
def VerSegSoci(request, pk):
	if request.user.is_authenticated():
		segu_social = get_object_or_404(Segu_Social, pk=pk)
		return render(request, "panel/seguro_social/Versegsoc.html", {"segu_social":segu_social})
	else:
		return render(request, "z-autentificacion.html", {})
#<----- ----->
def EditarSegSoci(request,pk):
	if request.user.is_authenticated():
		jubi = get_object_or_404(Segu_Social, pk=pk)
		if request.method == "POST":
			form = SeguroUpdate(request.POST, instance=jubi)
			if form.is_valid():
				vaca = form.save(commit=False)
				vaca.save()
				if request.POST['estatus'] == 'Procesando':
					mensaje = 'esta siendo procesada.'
				elif request.POST['estatus'] == 'Rechazada':
					mensaje = 'rechazada.'
				else:
					mensaje = 'aprobada con éxito.'
				Notificacion(
					usuario=jubi.expediente.trabajador.usuario,
					contenido="Su solicitud de registro al IVSS a sido {}".format(mensaje),
					tipo="trabajador",
					url="/constancias/ver_segsoc/"+str(vaca.pk)
					).save()
			else:
				messages.add_message(request, messages.INFO, "Ocurrio un problema al actualizar los datos.")
				return redirect('Constancias:verSegSoc',pk)
			messages.add_message(request, messages.INFO, "Estatus actualizo con éxito.")
			return redirect('Constancias:verSegSoc',pk)
	else:
		return render(request, "restringido.html", {})


# <-----CRONOLOGICO----->
def AggCronologico(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = CronologicoForm(request.POST)
			if form.is_valid():
				form.save()
				
			else:
				return render(request, "panel/archivista/addcrono.html", {"crono":form})
			return HttpResponseRedirect("/trabaexpe/mensaje")
		else:
			form = CronologicoForm()
		return render(request,'panel/archivista/addcrono.html',{'crono':form})
	else:
		return render(request, "restringido.html", {})

def ListCrono(request):
	crono = Cronologico.objects.all()
	context = {'crono':crono}
	return render(request,'panel/archivista/Listcrono.html', context)

# <-----VER----->
def VerCrono(request, pk):
	if request.user.is_authenticated():
		crono = get_object_or_404(Cronologico, pk=pk)
		return render(request, "panel/archivista/Vercrono.html", {"crono":crono})
	else:
		return render(request, "z-autentificacion.html", {})
#<----- ----->

# <-----VACACIONES----->
def AggVacaciones(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = VacacionesForm(request.POST)
			trabajador = Trabajador.objects.get(usuario=request.user)
			expediente = Expedientes.objects.get(trabajador=trabajador)
			periodo = Periodo.objects.filter(expediente=expediente)
			des = Descan_Trimes.objects.filter(expediente=expediente).exclude(estatus='Rechazada')
			if des.exists():
				descansos = Descan_Trimes.objects.filter(expediente=expediente).exclude(estatus='Rechazada').last()
				if descansos != None:
					fec = request.POST['fech_inic'].split('/')
					fecha = datetime.strptime(fec[2]+'-'+fec[1]+'-'+fec[0], '%Y-%m-%d').date()
					if fecha >= descansos.fech_solici and fecha <= descansos.fech_fin:
						messages.add_message(request, messages.INFO, "Solicitud no registrada porque ya posee una solicitud de descanso trimestral en la fecha introducida.")
						return redirect('Constancias:Aggvaca')
			if form.is_valid():
				fom = form.save()
				fecha = datetime.now().strftime('%d%m%Y')
				codigo = str(fecha)+str(fom.pk)
				Vacaciones.objects.filter(pk=fom.pk).update(cod_vaca=codigo)
				
				Periodo.objects.filter(pk=fom.periodo.pk).update(estatus=True)
				Notificacion(
					usuario=trabajador.usuario,
					contenido="El trabajador {} ha solicitado disfrutar de sus vacaciones".format(trabajador.nomb_trab),
					tipo="vacaciones",
					url="/constancias/ver_vaca/"+str(fom.pk)
					).save()
				#is_trabajador = request.user.first_name
				#seguimientos = Seguimiento.objects.filter(expedientes_id=save.relacion1_id).update(cita=save, fecha_cit=date, user_cit=user, cita_fecha_asig=save.fecha, cita_tranom_asig=save.relacion.nombre, cita_traape_asig=save.relacion.apellido)		

				#expediente = Expedientes.objects.get(trabajador=request.user)
			else:
				return render(request, "panel/vacaciones/addVaca.html", {"vaca":form})
			messages.add_message(request, messages.INFO, "Solicitud registrada con éxito.")
			return redirect('Constancias:Aggvaca')
		else:
			form = VacacionesForm()

		return render(request,'panel/vacaciones/addvaca.html',{'vaca':form})
	else:
		return render(request, "restringido.html", {})

def periodo(request):
	data = []
	trabajador = Trabajador.objects.get(usuario=request.user)
	expediente = Expedientes.objects.get(trabajador=trabajador)
	fecha = datetime.now().strftime('%Y')
	if request.user.is_staff:
		if request.method == 'POST':
			tipo = request.POST['tipo_vaca']
			if(tipo == 'Reglamentarias'):
				per = Periodo.objects.filter(expediente=expediente,adelanto=False,estatus=False).order_by('-periodo').exclude(periodo__contains=fecha)
				if(len(per) >0):
					err = 'No puede seleccionar esta opción, Tiene vacaciones pendiente por disfrutar.'
					data.append({"id_valid":False,"err":err})
				else:
					per = Periodo.objects.filter(periodo__contains=fecha,adelanto=False,expediente=expediente).order_by('-periodo')
					if(len(per) == 0):
						err = 'No puede seleccionar esta opción, aún no le corresponde disfrutar de sus vacaciones reglamentarias.'
						data.append({"id_valid":False,"err":err})
					if(per.filter(estatus=True)):
						err = 'No puede seleccionar esta opción, ya solicito una vacación en el periodo reglamentario.'
						data.append({"id_valid":False,"err":err})
					else:
						data1 = []
						for i in per:
							fecha = str(int(str(i.periodo).split('-')[0])-1)+'-'+str(i.periodo).split('-')[0]
							option = fecha+' '+str(i.dias)+' dias'
							data1.append({'id':i.id,"option":option,"dias":i.dias})
						data.append({"is_valid":True,"data":data1})
			if(tipo == 'Atrasadas'):
				
				per = Periodo.objects.filter(expediente=expediente,adelanto=False,estatus=False).order_by('-periodo').exclude(periodo__contains=fecha)

				if(len(per) == 0):
					err = 'No puede seleccionar esta opción, no posee vacaciones atrasadas por disfrutar.'
					data.append({"id_valid":False,"err":err})
				else:
					data1 = []
					for i in per:
						fecha = str(int(str(i.periodo).split('-')[0])-1)+'-'+str(i.periodo).split('-')[0]
						option = fecha+' '+str(i.dias)+' dias'
						data1.append({'id':i.id,"option":option,"dias":i.dias})
					data.append({"is_valid":True,"data":data1})

			if(tipo == 'Adelantadas'):
				
				per1 = Periodo.objects.filter(expediente=expediente,adelanto=False,estatus=False).order_by('-periodo').exclude(periodo__contains=fecha)
				if(len(per1) >0):
					err = 'No puede seleccionar esta opción, Tiene vacaciones pendiente por disfrutar.'
					data.append({"id_valid":False,"err":err})
				else:
					per = Periodo.objects.filter(periodo__contains=fecha,expediente=expediente,adelanto=False)
					if(len(per) == 1):
						err = 'No puede seleccionar esta opción, le corresponden disfrutar sus vacaciones de mánera reglamentaria.'
						data.append({"id_valid":False,"err":err})
					if(per.filter(estatus=True)):
						err = 'No puede seleccionar esta opción, ya solicito una vacación en el periodo reglamentario.'
						data.append({"id_valid":False,"err":err})
					else:
						data1 = []
						peri = Periodo.objects.filter(periodo__contains=fecha,expediente=expediente,adelanto=True)
						if(peri.filter(estatus=True)):
							err = 'No puede seleccionar esta opción, ya solicito un adelanto de vacaciones.'
							data.append({"id_valid":False,"err":err})
						else:
							fec1 = datetime.now().date()
							peri = Periodo.objects.filter(expediente=expediente)
							if peri:
								if  fec1 > peri.first().periodo:
									fec = str(peri.first().periodo).split('-')
									fech = str(int(fec[0])+1)+'-'+str(fec[1])+'-'+str(fec[2])
									periodo =Periodo(periodo=fech,expediente=expediente,dias=20,adelanto=True,estatus=False)
									periodo.save()
									peri = Periodo.objects.filter(pk=periodo.pk)
									for i in peri:
										fecha = str(int(str(i.periodo).split('-')[0])-1)+'-'+str(i.periodo).split('-')[0]
										option = fecha+' '+str(i.dias)+' dias'
										data1.append({'id':i.id,"option":option,"dias":i.dias})
								else:
									for i in peri:
										fecha = str(int(str(i.periodo).split('-')[0])-1)+'-'+str(i.periodo).split('-')[0]
										option = fecha+' '+str(i.dias)+' dias'
										data1.append({'id':i.id,"option":option,"dias":i.dias})

							else:
								fec = str(trabajador.fech_ing_inst).split('-')
								print(int(fec[0])+1)
								fech = str(int(fec[0])+1)+'-'+str(fec[1])+'-'+str(fec[2])
								periodo =Periodo(periodo=fech,expediente=expediente,dias=20,adelanto=True,estatus=False)
								periodo.save()
								peri = Periodo.objects.filter(pk=periodo.pk)
								for i in peri:
									fecha = str(int(str(i.periodo).split('-')[0])-1)+'-'+str(i.periodo).split('-')[0]
									option = fecha+' '+str(i.dias)+' dias'
									data1.append({'id':i.id,"option":option,"dias":i.dias})

						data.append({"is_valid":True,"data":data1})


				

			return JsonResponse(data,safe=False)
		else:
			return JsonResponse(data,safe=False)
	else:
		return render(request, "restringido.html", {})

def RecibirVacaciones(request,pk):
	if request.user.is_authenticated():
		reci = get_object_or_404(Vacaciones, pk=pk)
		form = ""
		user = None
		if request.method == "POST":
			form = VacacionesUpdate(request.POST, instance=reci)
			if form.is_valid():
				reci1 = form.save(commit=False)
				reci.save()
				if request.POST['estatus'] == 'Rechazada':
					mensaje = 'rechazada.'
				else:
					mensaje = 'aprobada con éxito.'
				Notificacion(
					usuario=reci.periodo.expediente.trabajador.usuario,
					contenido="Su solicitud de vacaciones a sido {}".format(mensaje),
					tipo="trabajador",
					url="/constancias/ver_vaca/"+str(reci1.pk)
					).save()
				
				messages.add_message(request, messages.INFO, "Vacacion Actualizada con éxito.")
				return redirect('Constancias:verVaca',pk)
			else:
				messages.add_message(request, messages.INFO, "Error al actualizar el estatus.")

				return redirect('Constancias:verVaca',pk)

			
		else:
			return redirect('Constancias:verVaca',pk)

	else:
		return render(request, "z-autentificacion.html", {})

def EsperaVacaciones(request,pk):
	if request.user.is_authenticated():
		espe = get_object_or_404(Vacaciones, pk=pk)
		form = ""
		user = None
		if request.method == "POST":
			form = VacacionFormss(request.POST, instance=espe)
			if form.is_valid():
				user = request.user.username
				espe = form.save(commit=False)
				espe.save()
				date = time.strftime("%d / %m / %Y")
				if espe.espera == True:
					vacaciones = Vacaciones.objects.filter(expediente_id=espe.expediente).update(fecha_pof=date, user_pof=user)
			else:
				return render(request, "panel/vacaciones/espera.html",{"edit_vaca":form, "vaca":espe})
			return HttpResponseRedirect("/registro/notificacion")	
		else:
			form = VacacionFormss(instance=espe)
		return render(request, "panel/vacaciones/espera.html",{"edit_vaca":form, "vaca":espe, "pk":pk})
	else:
		return render(request, "z-autentificacion.html", {})


# <-----LISTADO----->
def ListVaca(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		periodo = Periodo.objects.filter(expediente=expediente)
		vaca = Vacaciones.objects.filter(periodo__in=periodo).order_by('id')
	else:
		vaca = Vacaciones.objects.all().order_by('id')
	print(vaca)
	context = {'vaca':vaca}
	return render(request,'panel/vacaciones/ListVaca.html', context)

# <-----EDITAR----->
def EditarVaca(request,pk):
	if request.user.is_authenticated():
		vaca = get_object_or_404(Vacaciones, pk=pk)
		if request.method == "POST":
			form = VacacionesForm(request.POST, instance=vaca)
			if form.is_valid():
				vaca1 = form.save(commit=False)
				vaca.save()
				
			else:
				return render(request, "panel/vacaciones/Editvaca.html",{"edit_vaca": form})
			return HttpResponseRedirect("/trabaexpe/mensaje")
		else:
			form = VacacionesForm(instance=vaca)
		return render(request, 'panel/vacaciones/Editvaca.html', {"edit_vaca": form})
	else:
		return render(request, "restringido.html", {})
#<----- ----->
# <-----VER----->
def VerVaca(request, pk):
	if request.user.is_authenticated():
		vaca = get_object_or_404(Vacaciones, pk=pk)
		return render(request, "panel/vacaciones/Vervaca.html", {"vaca":vaca})
	else:
		return render(request, "z-autentificacion.html", {})
#<----- ----->

# <-----JUBILADO----->
def AggJubilacion(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		if request.method == 'POST':
			form = JubilacionForm(request.POST)
			if form.is_valid():
				fom =form.save()
				fecha = datetime.now().strftime('%d%m%Y')
				codigo = str(fecha)+str(fom.pk)
				Jubilacion.objects.filter(expediente=expediente).update(cod_jubila=codigo)
				Notificacion(
					usuario=trabajador.usuario,
					contenido="El trabajador {} ha solicitado su jubilación".format(trabajador.nomb_trab),
					tipo="jubilacion",
					url="/constancias/ver_jubi/"+str(fom.pk)
					).save()

				# expediente = Expediente.objects.filter(expediente_id=save.cedula).update(vaca=save)
			else:
				return render(request, "panel/jubilacion/addJubi.html", {"jubi":form})
			messages.add_message(request, messages.INFO, "Solicitud registrada con éxito.")
			return redirect('Constancias:Aggjubi')
		else:
			jubilacion = Jubilacion.objects.filter(expediente=expediente).exclude(estatus="Rechazada")
			if jubilacion.exists():
				jubilacion = jubilacion.first()
			else:
				jubilacion = False
		return render(request,'panel/jubilacion/addJubi.html',{'expediente':expediente,"jubilacion":jubilacion})
	else:
		return redirect('/trabaexpe/admin/')

def ListJubi(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		jubi = Jubilacion.objects.filter(expediente=expediente).order_by('id')
		print('entro aqui')
	else:
		jubi = Jubilacion.objects.all().order_by('id')
	context = {'jubi':jubi}
	return render(request,'panel/jubilacion/ListJubi.html', context)

# <-----VER----->
def VerJubi(request, pk):
	if request.user.is_authenticated():
		jubi = get_object_or_404(Jubilacion, pk=pk)
		return render(request, "panel/jubilacion/Verjubi.html", {"jubi":jubi})
	else:
		return render(request, "z-autentificacion.html", {})

def EditarJubi(request,pk):
	if request.user.is_authenticated():
		jubi = get_object_or_404(Jubilacion, pk=pk)
		if request.method == "POST":
			form = JubilacionUpdate(request.POST, instance=jubi)
			if form.is_valid():
				vaca = form.save(commit=False)
				vaca.save()
				if request.POST['estatus'] == 'Procesando':
					mensaje = 'puesta en proceso.'
				elif request.POST['estatus'] == 'Rechazada':
					mensaje = 'rechazada.'
				else:
					mensaje = 'aprobada con éxito.'
				Notificacion(
					usuario=jubi.expediente.trabajador.usuario,
					contenido="Su solicitud de jubilación a sido {}".format(mensaje),
					tipo="trabajador",
					url="/constancias/ver_jubi/"+str(vaca.pk)
					).save()
			else:
				messages.add_message(request, messages.INFO, "Ocurrio un problema al actualizar los datos.")
				return redirect('Constancias:verJubi',pk)
			messages.add_message(request, messages.INFO, "Estatus actualizo con éxito.")
			return redirect('Constancias:verJubi',pk)
	else:
		return render(request, "restringido.html", {})
#<----- ----->

# <-----PENSION----->
def AggPension(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		if request.method == 'POST':
			form = PensionForm(request.POST)
			if form.is_valid():
				fom =form.save()
				fecha = datetime.now().strftime('%d%m%Y')
				codigo = str(fecha)+str(fom.pk)
				Pension.objects.filter(expediente=expediente).update(cod_pen=codigo)
				Notificacion(
					usuario=trabajador.usuario,
					contenido="El trabajador {} ha solicitado su pensión".format(trabajador.nomb_trab),
					tipo="seguro",
					url="/constancias/ver_pen/"+str(fom.pk)
					).save()

				# expediente = Expediente.objects.filter(expediente_id=save.cedula).update(vaca=save)
			else:
				return render(request, "panel/pension/addPen.html", {"jubi":form})
			messages.add_message(request, messages.INFO, "Solicitud registrada con éxito.")
			return redirect('Constancias:Aggpen')
		else:
			pension = Pension.objects.filter(expediente=expediente).exclude(estatus="Rechazada")
			if pension.exists():
				pension = pension.first()
			else:
				pension = False
		return render(request,'panel/pension/addPen.html',{'expediente':expediente,"pension":pension})
	else:
		return redirect('/trabaexpe/admin/')

def ListPen(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		pen = Pension.objects.filter(expediente=expediente).order_by('id')
	else:
		pen = Pension.objects.all().order_by('id')
	context = {'pen':pen}
	return render(request,'panel/pension/ListPen.html', context)

# <-----VER----->
def VerPen(request, pk):
	if request.user.is_authenticated():
		pen = get_object_or_404(Pension, pk=pk)
		return render(request, "panel/pension/Verpen.html", {"jubi":pen})
	else:
		return render(request, "z-autentificacion.html", {})

def EditarPen(request,pk):
	if request.user.is_authenticated():
		jubi = get_object_or_404(Pension, pk=pk)
		if request.method == "POST":
			form = PensionUpdate(request.POST, instance=jubi)
			if form.is_valid():
				vaca = form.save(commit=False)
				vaca.save()
				if request.POST['estatus'] == 'Procesando':
					mensaje = 'puesta en proceso.'
				elif request.POST['estatus'] == 'Rechazada':
					mensaje = 'rechazada.'
				else:
					mensaje = 'aprobada con éxito.'
				Notificacion(
					usuario=jubi.expediente.trabajador.usuario,
					contenido="Su solicitud de pensión a sido {}".format(mensaje),
					tipo="trabajador",
					url="/constancias/ver_pen/"+str(vaca.pk)
					).save()
			else:
				messages.add_message(request, messages.INFO, "Ocurrio un problema al actualizar los datos.")
				return redirect('Constancias:verPen',pk)
			messages.add_message(request, messages.INFO, "Estatus actualizo con éxito.")
			return redirect('Constancias:verPen',pk)
	else:
		return render(request, "restringido.html", {})

def AggRetiro(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		if request.method == 'POST':
			form = RetiroForm(request.POST)
			if form.is_valid():
				fom =form.save()
				Notificacion(
					usuario=trabajador.usuario,
					contenido="El trabajador {} ha solicitado cambio de institución.".format(trabajador.nomb_trab),
					tipo="jubilacion",
					url="/constancias/ver_reti/"+str(fom.pk)
					).save()
			else:
				return render(request, "panel/jubilacion/addReti.html", {"jubi":form})
			messages.add_message(request, messages.INFO, "Solicitud registrada con éxito.")
			return redirect('Constancias:AggRetiro')
		else:
			cambio = Cambio.objects.filter(expediente=expediente).exclude(estatus="Rechazada")
			if cambio.exists():
				cambio = cambio.first()
			else:
				cambio = False
		return render(request,'panel/jubilacion/addReti.html',{'expediente':expediente,"cambio":cambio})
	else:
		return redirect('/trabaexpe/admin/')


def ListReti(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		cambio = Cambio.objects.filter(expediente=expediente).order_by('id')
	else:
		cambio = Cambio.objects.all().order_by('id')
	context = {'cambio':cambio}
	return render(request,'panel/jubilacion/ListReti.html', context)

def VerReti(request, pk):
	if request.user.is_authenticated():
		cambio = get_object_or_404(Cambio, pk=pk)
		return render(request, "panel/jubilacion/Verreti.html", {"cambio":cambio})
	else:
		return render(request, "z-autentificacion.html", {})

def EditarReti(request,pk):
	if request.user.is_authenticated():
		jubi = get_object_or_404(Cambio, pk=pk)
		if request.method == "POST":
			form = CambioUpdate(request.POST, instance=jubi)
			if form.is_valid():
				vaca = form.save(commit=False)
				vaca.save()
				if request.POST['estatus'] == 'Rechazada':
					mensaje = 'rechazada.'
				else:
					mensaje = 'aprobada con éxito.'
				Notificacion(
					usuario=jubi.expediente.trabajador.usuario,
					contenido="Su solicitud de cambio de institución a sido {}".format(mensaje),
					tipo="trabajador",
					url="/constancias/ver_reti/"+str(vaca.pk)
					).save()
			else:
				messages.add_message(request, messages.INFO, "Ocurrio un problema al actualizar los datos.")
				return redirect('Constancias:verreti',pk)
			messages.add_message(request, messages.INFO, "Estatus actualizo con éxito.")
			return redirect('Constancias:verreti',pk)
	else:
		return render(request, "restringido.html", {})


# <-----DESCANSO/TRIMESTRAL----->
def AggDescan_Trimes(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = Descan_TrimesForm(request.POST)
			trabajador = Trabajador.objects.get(usuario=request.user)
			expediente = Expedientes.objects.get(trabajador=trabajador)
			fecha = datetime.now().strftime('%Y')
			descanso = Descan_Trimes.objects.filter(expediente=expediente).exclude(estatus="Rechazada")
			if descanso.exists():
				fec = datetime.strptime(str(request.POST['fech_solici']), '%d/%m/%Y').date()
				resta = fec-descanso.first().fech_solici
				if resta.days < 90 :
					messages.add_message(request, messages.INFO, "No puedes solicitar un descanso, aún no le corresponde.")
					return redirect('Constancias:Aggdes_trim')

			periodo = Periodo.objects.filter(periodo__contains=fecha,expediente=expediente)
			if periodo.exists():
				vacaciones = Vacaciones.objects.filter(periodo=periodo).exclude(estatus='Rechazada').last()
				vacaciones1 = Vacaciones.objects.filter(periodo=periodo).exclude(estatus='Rechazada')
				if vacaciones != None:
					fec = request.POST['fech_solici'].split('/')
					fecha = datetime.strptime(fec[2]+'-'+fec[1]+'-'+fec[0], '%Y-%m-%d').date()
					if fecha >= vacaciones.fech_inic and fecha <= vacaciones.fech_culm:
						messages.add_message(request, messages.INFO, "Solicitud no registrada porque ya posee una solicitud de vacaciones en la fecha introducida.")
						return redirect('Constancias:Aggdes_trim')
				if vacaciones1.filter(estatus='Aprobada').exists():
					messages.add_message(request, messages.INFO, "Solicitud no registrada porque ya disfruto de vacaciones en este año.")
					return redirect('Constancias:Aggdes_trim')
			if form.is_valid():
				fom =form.save()
				fecha = datetime.now().strftime('%d%m%Y')
				codigo = str(fecha)+str(fom.pk)
				expediente = Descan_Trimes.objects.filter(pk=fom.pk ).update(expediente=expediente,cod_des_tri=codigo)
				Notificacion(
					usuario=trabajador.usuario,
					contenido="El trabajador {} ha solicitado disfrutar de un descanso trimestral".format(trabajador.nomb_trab),
					tipo="vacaciones",
					url="/constancias/ver_des/"+str(fom.pk)
					).save()
				messages.add_message(request, messages.INFO, "Solicitud registrada con éxito.")
				return redirect('Constancias:Aggdes_trim')
			else:
				return render(request, "panel/descansoTrimestral/adddes.html", {"des_tri":form})
		else:
			form = Descan_TrimesForm()
		return render(request,'panel/descansoTrimestral/adddes.html',{'des_tri':form})
	else:
		return render(request, "restringido.html", {})

def ListDescan_Trimes(request):
	if request.user.is_trabajador:
		trabajador = Trabajador.objects.get(usuario=request.user)
		expediente = Expedientes.objects.get(trabajador=trabajador)
		des_tri = Descan_Trimes.objects.filter(expediente=expediente)
	else:
		des_tri = Descan_Trimes.objects.all()
	context = {'des_tri':des_tri}
	return render(request,'panel/descansoTrimestral/ListDes.html', context)

# <-----VER----->
def VerDescan_Trimes(request, pk):
	if request.user.is_authenticated():
		des_tri = get_object_or_404(Descan_Trimes, pk=pk)
		if request.method == 'POST':
			form = Descan_TrimesFormUpdate(request.POST,instance=des_tri)
			if form.is_valid():
				fom =form.save()
				if request.POST['estatus'] == 'Rechazada':
					mensaje = 'rechazada.'
				else:
					mensaje = 'aprobada con éxito.'
				Notificacion(
					usuario=des_tri.expediente.trabajador.usuario,
					contenido="Su solicitud de descanso trimestral a sido {}".format(mensaje),
					tipo="trabajador",
					url="/constancias/ver_des/"+str(fom.pk)
					).save()
				messages.add_message(request, messages.INFO, "Descanso trimestral Actualizado con éxito.")
				return redirect('Constancias:verDes',fom.pk)
			else:
				return render(request, "panel/descansoTrimestral/Verdestri.html", {"form":form,"des_tri":des_tri})
		else:
			form = Descan_TrimesFormUpdate(instance=des_tri)
		return render(request, "panel/descansoTrimestral/Verdestri.html", {"form":form,"des_tri":des_tri})
	else:
		return render(request, "z-autentificacion.html", {})
#<----- ----->

# <-----EVALUACION----->
def AggEvaluacion(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = EvaluacionForm(request.POST)
			if form.is_valid():
				form.save()
				# expediente = Expediente.objects.filter(expediente_id=save.cedula).update(vaca=save)
			else:
				return render(request, "panel/archivista/addeva.html", {"eva":form})
			return HttpResponseRedirect("/trabaexpe/mensaje")
		else:
			form = EvaluacionForm()
		return render(request,'panel/archivista/addeva.html',{'eva':form})
	else:
		return render(request, "restringido.html", {})

def ListEvaluacion(request):
	eva = Evaluacion.objects.all()
	context = {'eva':eva}
	return render(request,'panel/archivista/ListEva.html', context)

# <-----VER----->
def VerEvaluacion(request, pk):
	if request.user.is_authenticated():
		eva = get_object_or_404(Evaluacion, pk=pk)
		return render(request, "panel/archivista/Vereva.html", {"eva":eva})
	else:
		return render(request, "z-autentificacion.html", {})
#<----- ----->

# Mensaje de que el Registro fue Exitoso -----------------------------------------------------------------------------
def Mensaje(request):
	return render(request, "panel/mensaje.html", {})
#<----- ----->

# <------ REPORTES ------>

# PDF de Trabajadores -----------------------------------------------------------------------------
#INDIVIDUAL

class ReportePersonasPDF(View):
	def cabecera(self,pdf,doc):
		fecha = datetime.now().strftime('%d/%m/%Y')
		mes = datetime.now().strftime('%m/%Y')
		title = "Constancia de Trabajo - Deparweb"
		pdf.setTitle(title)
		#Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
		archivo_imagen = settings.MEDIA_ROOT+'static/images/cintillo/1.png'
		#Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 30, 740, width=540,height=100,preserveAspectRatio=True)
		pdf.setFont("Helvetica", 16)
		#Dibujamos una cadena en la ubicación X,Y especificada
		pdf.setFont("Helvetica-Bold", 20)
		pdf.drawString(220, 710, "CONSTANCIA")
		
		# user = get_object_or_404(User)
		user = request.user
		p = User.objects.filter(is_trabajador=user.is_trabajador)
		
		#traba = Trabajador.objects.filter(id=)
		
		ta_c = ParagraphStyle('parrafos', 
							alignment = TA_CENTER,
							fontSize = 13,
							fontName="Helvetica-Bold",
							)	
		ta_l = ParagraphStyle('parrafos', 
							alignment = TA_LEFT,
							fontSize = 13,
							fontName="Helvetica",
							leading = 18,
							leftIndent = 50,
							)
		ta_l7 = ParagraphStyle('parrafos', 
							alignment = TA_LEFT,
							fontSize = 7,
							fontName="Helvetica-Bold",
							)
		ta_r = ParagraphStyle('parrafos', 
							alignment = TA_RIGHT,
							fontSize = 18,
							fontName="Helvetica-Bold",
							)
		setFont = Paragraph(
			u"Quien suscribe, Jefe de Recursos Humanos del Hospital Universitario “Dr. Miguel Oraá” de Guanare, por medio de la presente hace constar que la Ciudadana:"+str(p.nomb_trab+" "+p.ape_trab) ,ta_l)
		w, h = setFont.wrap(doc.width -30, doc.topMargin)
		setFont.drawOn(pdf, 35, doc.height -45, + doc.topMargin +15)

		setFont2 = Paragraph(
			u"Constancia que se expide para fines legales en la ciudad de Guanare, a los 17  Días del mes "+str(mes) ,ta_l)
		w, h = setFont2.wrap(doc.width -30, doc.topMargin)
		setFont2.drawOn(pdf, 35, doc.height -150, + doc.topMargin +15)
		
		footer6 = Paragraph("Fecha de expedición: "+str(fecha),ta_l7)
		w, h = footer6.wrap(doc.width -200, doc.bottomMargin) 
		footer6.drawOn(pdf,doc.height -580, doc.topMargin -95, h)


	def get(self, request, *args, **kwargs):
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = BytesIO()
		

		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		
		doc = SimpleDocTemplate(buffer,
			pagesizes=letter,
			rightMargin = 20,
			leftMargin= 50,
			topMargin=111,
			bottomMargin=85,
			paginate_by=0,
		)
		#Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf,doc)
		#Con show page hacemos un corte de página para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response

class NumberedCanvas(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []
 

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()
 

	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)
 
 
	def draw_page_number(self, page_count):
		self.setFont("Helvetica-Bold", 7)
		self.drawRightString(201 * mm, 4 * mm + (0.1 * inch),"Página %d de %d" % (self._pageNumber, page_count))


#Achivista ----------------------------------------------
def VacacionesView(request):
	if request.method == 'POST':
		form  = VacaFormArc(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/trabaexpe/admin/')
		else:
			form = VacaFormArc(request.POST)
			return render(request,'panel/archivista/addvaca.html',{"form":form})
	else:
		form = VacaFormArc()
	return render(request,'panel/archivista/addvaca.html',{"form":form})

#Achivista ----------------------------------------------
def PeriodoView(request):
	if request.method == 'POST':
		form  = PeriodoForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/trabaexpe/admin/')
		else:
			form = PeriodoForm(request.POST)
			return render(request,'panel/archivista/addperiodo.html',{"form":form})
	else:
		form = PeriodoForm()
	return render(request,'panel/archivista/addperiodo.html',{"form":form})
		
#addjubilacion

def JubilacionView(request):
	if request.method == 'POST':
		form  = JubiiForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/trabaexpe/admin/')
		else:
			form = JubiiForm(request.POST)
			return render(request,'panel/archivista/addjubilacion.html',{"form":form})
	else:
		form = JubiiForm()
	return render(request,'panel/archivista/addjubilacion.html',{"form":form})

def SeguroView(request):
	if request.method == 'POST':
		form  = SeguroForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/trabaexpe/admin/')
		else:
			form = SeguroForm(request.POST)
			return render(request,'panel/archivista/addseguro.html',{"form":form})
	else:
		form = SeguroForm()
	return render(request,'panel/archivista/addseguro.html',{"form":form})