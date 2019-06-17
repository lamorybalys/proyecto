from .models import Notificacion

def notificacion(request):
	if request.user.is_authenticated():
		if request.user.is_trabajador:
			notificacion = Notificacion.objects.filter(tipo="trabajador",usuario=request.user).order_by('-id')[:3]
			pendientes = Notificacion.objects.filter(tipo="trabajador",usuario=request.user,estatus=False).order_by('-id')
			pen = len(pendientes)

		elif request.user.is_analista_social:
			notificacion = Notificacion.objects.filter(tipo="seguro").order_by('-id')[:3]
			pendientes = Notificacion.objects.filter(tipo="seguro",estatus=False).order_by('-id')
			pen = len(pendientes)
		
		elif request.user.is_analista_jubilacion:
			notificacion = Notificacion.objects.filter(tipo="jubilacion").order_by('-id')[:3]
			pendientes = Notificacion.objects.filter(tipo="jubilacion",estatus=False).order_by('-id')
			pen = len(pendientes)

		elif request.user.is_analista_vacaciones:
			notificacion = Notificacion.objects.filter(tipo="vacaciones").order_by('-id')[:3]
			pendientes = Notificacion.objects.filter(tipo="vacaciones",estatus=False).order_by('-id')
			pen = len(pendientes)
		elif request.user.is_superuser:
			notificacion = ''
			pen = ''

		else:
			notificacion = ''
			pen = ''
	else:
		notificacion = ''
		pen = ''
	return {'notificaciones':notificacion,'pendientes':pen}