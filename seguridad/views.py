from django.shortcuts import render
from django.views.generic.base import TemplateView
#Importo Mixins Login
from .mixins import LoginRequiredMixin,SuperUserMixinRequired

class IndexPageView(TemplateView):
	template_name = 'core/landing_page/index.html'

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,{'titulo':'Deprasoft'})

class IndexPagePanelView(LoginRequiredMixin,TemplateView):
	template_name = 'panel_admin/index.html'

class ProhibidoView(TemplateView):
	template_name = 'registration/prohibido.html'



