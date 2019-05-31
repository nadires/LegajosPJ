"""legajos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.dependencia.views import DependenciaLaboralCreate, DependenciaLaboralUpdate, HistorialTraslados


urlpatterns = [
    path('<int:pk>/nueva-dependencia/', DependenciaLaboralCreate.as_view(), name="dependencia_create"),
    path('<int:id_empleado>/modificar-dependencia/<int:pk>', DependenciaLaboralUpdate.as_view(), name="dependencia_update"),
    path('<int:pk>/historial-traslados/', HistorialTraslados.as_view(), name="historial_traslados"),

]
