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

from apps.persona.views import PersonaList, PersonaDetail, PersonaCreate, PersonaUpdate, PersonaDelete, ImagenesPersonaView, PersonaPDF, FamiliarAutocomplete
from apps.persona.api.views import PersonaModelViewSet, PersonaViewSet, PersonaViewSetReadOnly, PersonaApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('persona',PersonaModelViewSet, basename='persona')
router.register('readonly-viewset',PersonaViewSetReadOnly, basename='viewSetReadOnly')
router.register('viewset',PersonaViewSet, basename='personaviewset')
router.register('viewset/<int:pk>',PersonaViewSet, basename='personaviewset')
router.register('viewset/<string:apellido>',PersonaViewSet, basename='personaviewset')

urlpatterns = [
    path('', PersonaList.as_view(), name="persona_list"),
    path('<int:pk>/', PersonaDetail.as_view(), name="persona_detail"),
    path('nuevo/', PersonaCreate.as_view(), name="persona_create"),
    path('modificar/<int:pk>', PersonaUpdate.as_view(), name="persona_update"),
    path('eliminar/<int:pk>', PersonaDelete.as_view(), name="persona_delete"),
    path('<int:id_persona>/<int:id_seccion>/', ImagenesPersonaView.as_view(), name='imagenes_persona'),
    path('pdf/<int:pk>', PersonaPDF.as_view(), name="persona_pdf"),

    path('api/v1/', include(router.urls)),
    path('api/v1/apiview', PersonaApiView.as_view(), name="personaapiview"),

    path('familiar-autocomplete/', FamiliarAutocomplete.as_view(), name='familiar-autocomplete',),

]
