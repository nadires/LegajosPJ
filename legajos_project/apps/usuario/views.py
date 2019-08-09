from django.contrib.auth.views import LoginView

from .forms import LoginForm


class Login(LoginView):
    form_class = LoginForm
    template_name = 'base/login.html'
