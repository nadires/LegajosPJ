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


class Login(LoginView):
    template_name = 'base/login.html'


class Error404(TemplateView):
    template_name = 'base/error_404.html'
