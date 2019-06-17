from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from apps.constancias.models import *
from apps.constancias.forms import *
from seguridad.models import User,Notificacion
from seguridad.mixins import LoginRequiredMixin
import time
from django.views.generic import CreateView, TemplateView, View 
from django.views.defaults import page_not_found
from django.contrib import messages
#para trabajar con excel
import openpyxl
from django.http import JsonResponse

class NotificacionUpdate(LoginRequiredMixin,TemplateView):
	def post(self,request):
		estatus = Notificacion.objects.filter(id=request.POST['id'])
		estatus.update(estatus=1)
		return JsonResponse({"valid":True})

def mi_error_404(request):
    nombre_template = 'panel/404.html'
 
    return page_not_found(request, template_name=nombre_template)

# Create your views here.
def PanelAdministrativo(request):
    if request.user.is_authenticated():
        des_tri = Descan_Trimes.objects.all().order_by("id").reverse()[:5]
        jubi = Jubilacion.objects.all().order_by("id")
        traba = Trabajador.objects.all().order_by("id")
        vaca = Vacaciones.objects.all().order_by("id").reverse()[:5]
        expe = Expedientes.objects.all().order_by("id").reverse()[:5]
        seg_soci = Segu_Social.objects.all().order_by("id").reverse()[:5]
        crono = Cronologico.objects.all().order_by("id").reverse()[:5]
        eva = Evaluacion.objects.all().order_by("id").reverse()[:5]
        director = Directores.objects.all().order_by("id").reverse()[:5]
        return render(request, "panelAdmin/index.html", {"traba":traba,"des_tri":des_tri,"jubi":jubi, "vaca": vaca, "expe":expe, "seg_soci":seg_soci, "crono":crono, "eva":eva, "director":director})
    else:
        return render(request, "z-autentificacion.html", {})

  
#<-----AGREGAR EXPEDIENTES----->
def aggExpedientes(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = ExpedientesForm(request.POST)
			if form.is_valid():
				form = form.save()
				#expe = Expedientes.objects
				#trabajador = Trabajador.objects.filter(pk=form.trabajador)
				User.objects.filter(cedula=form.trabajador.usuario).update(is_active=True)
			else:
				return render(request, "panel/archivista/aggexpediente.html",{"expe":form})
			messages.add_message(request, messages.INFO, "Expediente registrado con éxito, El trabajador ya puede acceder al sistema.")
			return redirect('Trabaexpe:Aggexpe')
		else:
			form = ExpedientesForm()
		return render(request,'panel/archivista/aggexpediente.html',{'expe':form})
	else:
		return render(request, "restringido.html", {})

def ListExpediente(request):
	expe = Expedientes.objects.all()
	context = {'expe':expe}
	return render(request,'panel/archivista/Listexpe.html', context)

# <-----VER----->
def VerExpediente(request, pk):
	if request.user.is_authenticated():
		expe = get_object_or_404(Expedientes, pk=pk)
		traba = Trabajador.objects.filter(pk=pk)
		eva = Evaluacion.objects.filter(pk=pk)
		crono = Cronologico.objects.filter(pk=pk)
		des_tri = Descan_Trimes.objects.filter(pk=pk)
		vaca = Vacaciones.objects.filter(pk=pk)
		seg_soc = Segu_Social.objects.filter(pk=pk)
		jubi = Jubilacion.objects.filter(pk=pk)
		user = User.objects.filter(pk=pk)
		#terreno = Terreno.objects.all().filter(relacion__relacion1=pk)
		# seguimisento = Seguimiento.objects.all().filter(expediente__id=pk)
		return render(request, "panel/archivista/Verexpe.html", {"expe":expe, "traba":traba,
		"eva":eva, "crono":crono,"des_tri":des_tri,"vaca":vaca,"seg_soc":seg_soc,"jubi":jubi})
	else:
		return render(request, "z-autentificacion.html", {})

#<----- ----->

# <-----TRABAJADOR----->
def AggWorker(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = TrabajadorForm(request.POST)
			if form.is_valid():
				form = form.save()
				trabajador = Trabajador.objects.get(pk=form.pk)
				user = User(
					cedula=trabajador.cedu_trab,
					first_name=trabajador.nomb_trab,
					last_name=trabajador.ape_trab,
					is_trabajador=True,
					is_active=False,
					email=str(trabajador.cedu_trab)+'@gmail.com')
				user.set_password(str(trabajador.cedu_trab)+'1')
				user.save()
				Trabajador.objects.filter(pk=form.pk).update(usuario=user)
			else:
				return render(request, "panel/trabajador/aggtrabajador.html", {"traba":form})
			messages.add_message(request, messages.INFO, "Trabajador registrado con éxito.")
			return redirect('Trabaexpe:Aggm')
		else:
			form = TrabajadorForm()
		return render(request,'panel/trabajador/aggtrabajador.html',{'traba':form})
	else:
		return render(request, "restringido.html", {})

def ListTrabajador(request):
	worker = Trabajador.objects.all()
	context = {'worker':worker}
	return render(request,'panel/trabajador/Listworker.html', context)
# <-----VER----->
def VerTrabajador(request, pk):
	if request.user.is_authenticated():
		traba = get_object_or_404(Trabajador, pk=pk)
		return render(request, "panel/trabajador/Verworker.html", {"traba":traba})
	else:
		return render(request, "z-autentificacion.html", {})
#<----- ----->

#<-----DIRECTORES----->
def AggDirectores(request):
	if request.user.is_staff:
		if request.method == 'POST':
			form = DirectoresForm(request.POST)
			if form.is_valid():
				form.save()
			else:
				return render(request, "panel/aggdirector.html", {"director":form})
			return HttpResponseRedirect("/trabaexpe/mensaje")
		else:
			form = DirectoresForm()
		return render(request,'panel/aggdirector.html',{'director':form})
	else:
		return render(request, "restringido.html", {})
#<----- ----->


#LISTADO DE Directores
def ListDirectores(request):
	director = Directores.objects.all()
	context = {'director':director}
	return render(request, 'panel/Listdirec.html', context)
#<----- ----->

# <-----VER----->
def VerDirectores(request, pk):
	if request.user.is_authenticated():
		director = get_object_or_404(Directores, pk=pk)
		return render(request, "panel/Verdirector.html", {"director":director})
	else:
		return render(request, "z-autentificacion.html", {})

#<----- ----->

# <-----EDITAR DIRECTORES----->
def editarDirectores(request,pk):
	if request.user.is_authenticated():
		director = get_object_or_404(Directores, pk=pk)
		if request.method == "POST":
			form = DirectoresForm(request.POST, instance=director)
			if form.is_valid():
				director = form.save(commit=False)
				director.save()
			else:
				return render(request, "panel/Editdirect.html",{"ver_director": form})
			return HttpResponseRedirect("/trabaexpe/mensaje")
		else:
			form = DirectoresForm(instance=director)
		return render(request, 'panel/Editdirect.html', {"ver_director": form})
	else:
		return render(request, "restringido.html", {})
#<-----Anadir sueldo ----->
def aggesueldo(request):
	if request.user.is_staff:
		if request.method == "POST":
			excel_file = request.FILES["excel_file"]
			wb = openpyxl.load_workbook(excel_file)

			worksheet = wb["Hoja1"]
			excel_data = []

			for row in worksheet.iter_rows():
				row_data = []
				for cell in row:
					row_data.append(str(cell.value))
				excel_data.append(row_data)
			count = 0
			print(request.POST)
			tipo = request.POST["tipo"]
			
			for idx in range(1,len(excel_data)):
				if tipo == 'Empleados':
					cedula = excel_data[idx][3]
					sueldo = excel_data[idx][13]
					compensasion = excel_data[idx][14]
					profesionalizacion = excel_data[idx][26]
					antiguedad = excel_data[idx][27]
				if tipo == 'Medicos':
					cedula = excel_data[idx][3]
					sueldo = excel_data[idx][13]
					compensasion = '0,00'
					profesionalizacion = excel_data[idx][23]
					antiguedad = excel_data[idx][24]
				if tipo == 'Obreros':
					cedula = excel_data[idx][3]
					sueldo = excel_data[idx][13]
					compensasion = excel_data[idx][14]
					profesionalizacion = excel_data[idx][23]
					antiguedad = excel_data[idx][24]
				if len(cedula) == 8 or len(cedula) == 7 :
					trabajador = Trabajador.objects.filter(cedu_trab=cedula)
					if trabajador.exists():
						count +=1
						expediente = Expedientes.objects.get(trabajador=trabajador)
						suel = Sueldo(
							expediente=expediente,
							sueldo=sueldo,
							compensasion=compensasion,
							profesionalizacion=profesionalizacion,
							antiguedad=antiguedad)
						suel.save()


					 

			print(tipo)
			if count >0:
				messages.add_message(request, messages.INFO, "Sueldos actualizados con éxito, se actualizarón: "+str(count)+" sueldos.")
				return redirect('Trabaexpe:sueldo')
			else:
				messages.add_message(request, messages.INFO, "El archivo cargado no contiene trabajadores para actualizarle el sueldo.")
				return redirect('Trabaexpe:sueldo')
				
			return render(request, "panel/sueldo/aggsueldo.html",{})
		else:
			return render(request,'panel/sueldo/aggsueldo.html',{})
	else:
		return render(request, "restringido.html", {})
# Mensaje de Solicitud de Vacaciones -----------------------------------------------------------------------------
def SoliVaca(request):
	return render(request, "panel/solicitudes/soliciVaca.html", {})
#<----- ----->


# Mensaje de que el Registro fue Exitoso -----------------------------------------------------------------------------
def Mensaje(request):
	return render(request, "panel/mensaje.html", {})
#<----- ----->

def trabajador_pdf(request, pk):
# Obtenemos un queryset, para un determinado solicitante usando pk.
	try:
		trabajador = Trabajador.objects.get(pk=trabajador_id)
		trabajador1 = get_object_or_404(Director)
		director2 = trabajador1.nombre + ' ' + trabajador1.apellido
		print (director2)

		director14 = trabajador1.fecha_reso
		print(director14)

		director15 = trabajador1.resolucion
		print(director15)

	except Trabajador.DoesNotExist: # Si no existe llamamos a "pagina no encontrada".
		raise Http404("Trabajador does not exist")
		# Creamos un objeto HttpResponse con las cabeceras del PDF correctas.
	return render(request, "reporte/reportetrabajador.html", {'director15':director15,'director14':director14,'director2':director2,'trabajador':trabajador})
	response = HttpResponse(content_type='application/pdf')
	# Nos aseguramos que el navegador lo abra directamente.
	response['ContentDisposition']='filename="archivo.pdf'
	buffer = BytesIO()
	# Creamos el objeto PDF, usando el objeto BytesIO como si fuera un "archivo".
	p = canvas.Canvas(buffer)

	# Dibujamos cosas en el PDF. Aquí se genera el PDF.	
	# Consulta la documentación para una lista completa de funcionalidades.
	p.roundRect(0, 750, 694, 120, 20, stroke=0, fill=1)
	p.setFont('TimesBold',32)
	p.setFillColorRGB(1,1,1)
	

	# mostramos y guardamos el objeto PDF.
	p.showPage()
	p.save()
	# Traemos el valor del bufer BytesIO y devolvemos la respuesta.
	pdf = buffer.getvalue()
	# Cerramos el bufer
	buffer.close()
	response.write(pdf)
	return response
