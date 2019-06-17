from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic import CreateView, TemplateView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
#Importamos el formulario de autenticación de django
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from .forms import *
from .models import *
from .forms import *
# from apps.panel.forms import *

def Inicio(request):
    return render(request,'landing/index.html')


# CAMBIAR CONTRASEÑA
def CambioContraseña(request):
    return render(request,'panelAdmin/change_pass.html')

# Create your views here.
class Login(FormView):
    #Establecemos la plantilla a utilizar
    template_name = 'login/index.html'
    #Le indicamos que el formulario a utilizar es el formulario de autenticación de Django
    form_class = AuthenticationForm
    #Le decimos que cuando se haya completado exitosamente la operación nos redireccione a la url bienvenida de la aplicación personas
    success_url =  reverse_lazy("Trabaexpe:Admin")

    def dispatch(self, request, *args, **kwargs):
        #Si el usuario está autenticado entonces nos direcciona a la url establecida en success_url
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        #Sino lo está entonces nos muestra la plantilla del login simplemente
        else:
            # return HttpResponse(request, status=401) 
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

class LogoutView(FormView):
    def get(self, request):
            logout(request)
            return redirect('/login')
            

# class SignUpView(CreateView):
#     model = Perfil
#     form_class = SignUpForm

#     def form_valid(self, form):
#         '''
#         En este parte, si el formulario es 
#         valido guardamos lo que se obtiene de 
#         él y usamos authenticate para que el usuario 
#         incie sesión luego de haberse registrado y 
#         lo redirigimos al index
#         '''
#         form.save()
#         usuario = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         login(self.request, usuario)
#         return redirect('/')

def Olvido_Pass(request):
    return render(request,'login/recup_pass.html')

# class RegistroUsuario(CreateView):
#     model = User
#     template_name = "panelAdmin/añad_usu.html"
#     form_class= RegistroForm
#     success_url = reverse_lazy("Seguridad:Admin")

# @login_required(login_url='/Inicio')
# def NuevoPerfil(request):
#     usuario=request.user
#     if request.method == 'POST':
#         form = PerfilForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/NuevoPerfil/Registrado/')
#         else:
#             form = PerfilForm()
#             return render_to_response('perfil/perfil_form.html.html', {'form': form,'usuario':usuario},context_instance=RequestContext(request))

def Perfil(request):
    return render(request, 'perfiles/perfil.html', {})