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

from apps.empleado.views import EmpleadoList, EmpleadoListDowns, EmpleadoDetail, EmpleadoCreate, \
    EmpleadoUpdate, EmpleadoDown, EmpleadoRestore, EmpleadoPDF, exportar_excel
from apps.cargo.views import CargoCreate, CargoUpdate, FojaServicios
from apps.dependencia.views import DependenciaLaboralCreate, DependenciaLaboralUpdate, HistorialTraslados
from .api.views import EmpleadoModelViewSet, EmpleadoViewSet, EmpleadoViewSetReadOnly, \
                        EmpleadoApiView, EndpointDependencias
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('empleado',EmpleadoModelViewSet, basename='empleado')
router.register('readonly-viewset',EmpleadoViewSetReadOnly, basename='viewSetReadOnly')
router.register('viewset',EmpleadoViewSet, basename='empleadoviewset')
router.register('viewset/<str:pk>',EmpleadoViewSet, basename='empleadoviewset')
router.register('viewset/<string:apellido>',EmpleadoViewSet, basename='empleadoviewset')

urlpatterns = [
# ----------------------------------- EMPLEADO -----------------------------------------
    path('', EmpleadoList.as_view(), name="empleado_list"),
    path('<str:pk>/', EmpleadoDetail.as_view(), name="empleado_detail"),
    path('nuevo', EmpleadoCreate.as_view(), name="empleado_create"),
    path('modificar/<str:pk>', EmpleadoUpdate.as_view(), name="empleado_update"),
    path('baja/<str:pk>', EmpleadoDown.as_view(), name="empleado_down"),
    path('empleados-eliminados', EmpleadoListDowns.as_view(), name="empleado_list_downs"),
    path('restaurar/<str:pk>', EmpleadoRestore.as_view(), name="empleado_restore"),

# ----------------------------------- OTROS -----------------------------------------
#     path('<str:id_empleado>/<int:id_seccion>/', ImagenesEmpleadoView.as_view(), name='imagenes_empleado'),
    path('pdf/<str:pk>', EmpleadoPDF.as_view(), name="empleado_pdf"),

    path('api/v1/', include(router.urls)),
    path('api/v1/apiview', EmpleadoApiView.as_view(), name="empleadoapiview"),
    path('api/v1/dependencias', EndpointDependencias.as_view(), name="endpoint_dependencias"),

    path('exportar/', exportar_excel, name="exportar"),

    # path('dependencias-autocomplete/', DependenciasAutocomplete.as_view(), name='dependencias-autocomplete'),

    # path('familiar-autocomplete/', FamiliarAutocomplete.as_view(), name='familiar-autocomplete',),

]
