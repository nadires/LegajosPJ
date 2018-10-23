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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.persona.views import PersonaList, PersonaDetail, PersonaCreate, ImagenesPersonaView

urlpatterns = [
    path('', PersonaList.as_view(), name="persona_list"),
    path('<int:pk>/', PersonaDetail.as_view(), name="persona_detail"),
    path('nuevo/', PersonaCreate.as_view(), name="persona_create"),
    path('<int:id_persona>/<int:id_seccion>/', ImagenesPersonaView.as_view(), name='imagenes_persona'),
]
