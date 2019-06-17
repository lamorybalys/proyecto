from django.urls import path
from .views import *

core_urlpatterns = ([
    path('', IndexPageView.as_view(), name="home"),
    path('panel', IndexPagePanelView.as_view(), name="panel"),
    path('prohibido',ProhibidoView.as_view(),name="prohibido")
    path('crear_usuario', UsersCreateView.as_view(), name='crear_usuario'),

],"core")

