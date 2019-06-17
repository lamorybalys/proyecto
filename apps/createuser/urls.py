from django.conf.urls import url
from . import *
from .views import *


urlpatterns = [
	url(r'^$', Inicio, name="Inicio"),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    # url(r'^registrate/$', SignUpView.as_view(), name='sign_up'),
    url(r"^recupass$", Olvido_Pass, name="recupass"),
    # url(r'^registrar$', RegistroUsuario.as_view(), name="registrar"),
	url(r"^pass/$", CambioContraseña, name="Pass"),
    url(r'^perfil/$', Perfil, name="perfil"),

]