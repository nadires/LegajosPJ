from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

# @method_decorator(user_passes_test(lambda u:u.is_admin, login_url=reverse_lazy('login')), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class Home(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		from apps.empleado.models import Empleado	
		from datetime import date
		este_anio = str(date.today().year)+'-01-01'
		context['cantidad_empleados'] = Empleado.objects.all().count()
		context['ingresados_este_anio'] = Empleado.objects.all().filter(fecha_ingreso__gte=este_anio).count()
		context['titulo'] = "Inicio"
		context['Home'] = True
		return context


class Login(LoginView):
    template_name = 'base/login.html'


class Error404(TemplateView):
    template_name = 'base/error_404.html'
