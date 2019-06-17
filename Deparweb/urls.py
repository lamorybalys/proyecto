"""Deparweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm, password_reset_complete
from django.conf.urls import handler404
from apps.trabaexpe.views import mi_error_404

handler404 = mi_error_404
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("apps.createuser.urls", namespace="Createuser")),
    url(r'^constancias/',include("apps.constancias.urls", namespace="Constancias")),
    url(r'^reportes/',include("apps.reportes.urls", namespace="reportes")),
    url(r'^trabaexpe/',include ("apps.trabaexpe.urls", namespace="Trabaexpe")),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.*)/$', password_reset_confirm,{'template_name':'seguridad/password_reset_confirm.html'},
     name="password_reset_confirm"),
    url(r'^reset/done', password_reset_complete,{'template_name':'seguridad/password_reset_complete.html'},
     name="password_reset_complete"),
]
