from itertools import chain

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelChoiceField
from django import forms
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core import serializers
import json
from django.conf import settings
from datetime import datetime
from django.core.cache import cache

from apps.dependencia.models import DependenciaLaboral
from .models import Empleado
from apps.util.models import Seccion
from .forms import EmpleadoForm
from apps.cargo.forms import CargoForm
from apps.dependencia.forms import DependenciaLaboralForm

from easy_pdf.views import PDFTemplateResponseMixin

from dal import autocomplete
from django.utils.html import format_html

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


class EmpleadoList(ListView):
    model = Empleado
    template_name = 'empleado/listado_empleados.html'
    context_object_name = 'listado_empleados'
    queryset = Empleado.activos.all()

    def get_context_data(self, **kwargs):
        context = super(EmpleadoList, self).get_context_data(**kwargs)
        context['titulo'] = "Listado de Empleados"
        context['EmpleadoList'] = True
        return context


class EmpleadoListDowns(ListView):
    """
        Muestra el listado de empleados eliminados
    """
    model = Empleado
    template_name = 'empleado/listado_empleados_baja.html'
    context_object_name = 'listado_empleados_baja'
    queryset = Empleado.objects.filter(borrado=True)

    def get_context_data(self, **kwargs):
        context = super(EmpleadoListDowns, self).get_context_data(**kwargs)
        context['titulo'] = "Listado de Empleados de Baja"
        context['EmpleadoListDowns'] = True
        return context


class EmpleadoDetail(DetailView):
    model = Empleado
    template_name = 'empleado/detalle_empleado.html'
    context_object_name = 'empleado'

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetail, self).get_context_data(**kwargs)
        secciones = Seccion.objects.all() # Busco todas las secciones
        listado = []  # Listado que contendr?? los diccionarios
        # for seccion in secciones:  # Recorro el listado de secciones
        #     elemento = {
        #         'seccion': seccion}  # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
        #     id_empleado = self.kwargs.get('pk', 0) # Obtengo el id de la empleado
        #     elemento['cantidad_imagenes'] = seccion.cantidad_imagenes_por_seccion(id_empleado)
        #     listado.append(elemento)  # Agrego el diccionario a la lista a retornar

        context['seccion_list'] = listado

        context['cargo'] = self.object.cargos_empleado.filter(actual=True).first()
        context['dependencia'] = self.object.dependencias_empleado.filter(actual=True).first()

        context['EmpleadoDetail'] = True
        context['titulo'] = "Detalle del Empleado"
        return context


class EmpleadoCreate(SuccessMessageMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado/empleado_form.html'
    success_message = "??%(calculated_field)s con ??xito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super(EmpleadoCreate, self).get_context_data(**kwargs)
        context['titulo'] = "Agregar Empleado"
        context['EmpleadoCreate'] = True
        return context

    def form_valid(self, form):
        user = self.request.user
        instance = form.save(commit=False)
        instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        mensaje = ''
        if self.object.sexo == 'M':
            mensaje = 'El empleado '+self.object.nombre+' '+self.object.apellido+' fue agregado'
        else:
            mensaje = 'La empleada '+self.object.nombre+' '+self.object.apellido+' fue agregada'
        return self.success_message % dict(
            cleaned_data,
            calculated_field=mensaje,
        )


class EmpleadoUpdate(SuccessMessageMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado/empleado_form.html'
    success_message = "??%(calculated_field)s con ??xito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super(EmpleadoUpdate, self).get_context_data(**kwargs)
        context['titulo'] = "Modificar Empleado"
        context['EmpleadoUpdate'] = True
        return context

    def form_valid(self, form):
        user = self.request.user
        instance = form.save(commit=False)
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        if self.object.sexo == 'M':
            mensaje = 'El empleado '+self.object.nombre+' '+self.object.apellido+' fue actualizado'
        else:
            mensaje = 'La empleada '+self.object.nombre+' '+self.object.apellido+' fue actualizada'
        return self.success_message % dict(
            cleaned_data,
            calculated_field = mensaje,
        )


class EmpleadoDown(DeleteView):
    model = Empleado
    template_name = 'empleado/baja_empleado.html'
    success_url = reverse_lazy('empleado_list')
    context_object_name = 'empleado'

    def delete(self, request, *args, **kwargs):
        """
            Modifico el m??todo eliminar, haciendo que cambie los estados de borrado y activo
        """
        self.object = self.get_object()
        self.object.borrado = True
        self.object.activo = False
        self.object.fecha_baja = datetime.strptime(request.POST.get('fecha_baja'), "%d/%m/%Y")
        self.object.motivo_baja = request.POST.get('motivo')
        # print(self.object.fecha_baja)
        # Deber??a poner fecha de fin al cargo
        self.object.save()
        if self.object.sexo == 'M':
            mensaje = '??El empleado '+self.object.nombre+' '+self.object.apellido+' fue dado de baja con ??xito!'
        else:
            mensaje = '??La empleada '+self.object.nombre+' '+self.object.apellido+' fue dada de baja con ??xito!'
        messages.success(self.request, mensaje)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDown, self).get_context_data(**kwargs)
        context['cargo'] = self.object.cargos_empleado.filter(actual=True).first()
        context['dependencia'] = self.object.dependencias_empleado.filter(actual=True).first()
        context['EmpleadoDown'] = True
        context['titulo'] = "Baja Empleado"
        return context


class EmpleadoRestore(SuccessMessageMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado/empleado_form.html'
    success_message = "??%(calculated_field)s con ??xito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super(EmpleadoRestore, self).get_context_data(**kwargs)
        context['titulo'] = "Restaurar Empleado"
        context['EmpleadoRestore'] = True
        return context

    def form_valid(self, form):
        user = self.request.user
        instance = form.save(commit=False)
        instance.modified_by = user
        instance.activo = True
        instance.borrado = False
        instance.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        if self.object.sexo == 'M':
            mensaje = 'El empleado '+self.object.nombre+' '+self.object.apellido+' fue restaurado'
        else:
            mensaje = 'La empleada '+self.object.nombre+' '+self.object.apellido+' fue restaurada'
        return self.success_message % dict(
            cleaned_data,
            calculated_field = mensaje,
        )


def exportar_excel(request):
    # key_cache = request.GET.get('key_cache')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    return response


# class ListadoSeccionesView(View):
# 	def get(self, request, *args, **kwargs):
# 		from apps.empleado.models import Seccion
# 		secciones = Seccion.objects.all() # Busco todas las secciones 
# 		listado = [] # Listado que contendr?? los diccionarios
# 		for seccion in secciones: # Recorro el listado de secciones
# 			elemento = {} # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
# 			elemento['seccion'] = seccion
# 			id_empleado = self.kwargs.get('pk', 0) # Obtengo el id de la empleado
# 			elemento['cantidad_imagenes'] = seccion.cantidad_imagenes_por_seccion(id_empleado)
# 			listado.append(elemento) # Agrego el diccionario a la lista a retornar

# 		# context['seccion_list'] = listado
# 		return JsonResponse(listado)


# class ImagenesEmpleadoView(View):
#     def get(self, request, *args, **kwargs):
#         id_empleado = self.kwargs.get('id_empleado', 0)
#         id_seccion = self.kwargs.get('id_seccion', 0)
#         empleado = Empleado.objects.get(pk=id_empleado)
#         seccion = Seccion.objects.get(pk=id_seccion)
#         imagenes_list = ImagenEmpleado.objects.filter(empleado=empleado, seccion=seccion)
#         secciones = Seccion.objects.all()
#         listado = [] # Listado que contendr?? los diccionarios
#         for elem_seccion in secciones: # Recorro el listado de secciones
#             elemento = {'seccion': elem_seccion, 'cantidad_imagenes': elem_seccion.cantidad_imagenes_por_seccion(
#                 id_empleado)}  # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
#             listado.append(elemento) # Agrego el diccionario a la lista a retornar
#         context = {
#             'imagenes_list': imagenes_list,
#             'empleado' : empleado,
#             'seccion' : seccion,
#             'seccion_list' : listado,
#         }
#         return render(self.request, 'empleado/imagenes_empleado.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = ImagenForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             imagen = form.save(commit=False)
#             imagen.created_by = request.user
#             imagen.modified_by = request.user
#             imagen.save()
#             form.save_m2m()
#             data = {'mensaje':'Success', 'is_valid': True, 'name': imagen.imagen.name, 'url': imagen.imagen.url}
#         else:
#             data = {'mensaje':'Error', 'is_valid': False}
#         return JsonResponse(data)


class EmpleadoPDF(PDFTemplateResponseMixin, DetailView):
    model = Empleado
    template_name = 'empleado/pdf.html'
    context_object_name = 'empleado'
    base_url = 'file://{}/'.format(settings.STATIC_ROOT)
    download_filename = 'LegajoDigital.pdf'

    def get_context_data(self, **kwargs):
        context = super(EmpleadoPDF, self).get_context_data(**kwargs)
        id_empleado = self.kwargs.get('pk', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        # imagenes_list = ImagenEmpleado.objects.filter(empleado=empleado)
        # context['imagenes_list'] = imagenes_list
        return context


# class DependenciasAutocomplete(autocomplete.Select2QuerySetView):
# 	def get_queryset(self):
# 		circunscripciones = Circunscripcion.objects.all()
# 		unidades = Unidad.objects.all()
# 		organismos = Organismo.objects.all()
# 		dependencias = Dependencia.objects.all()
# 		direcciones = Direccion.objects.all()
# 		departamentos = Departamento.objects.all()
# 		divisiones = Division.objects.all()
#
# 		if self.q:
# 			circunscripciones = circunscripciones.filter(circunscripcion__icontains=self.q)
# 			unidades = unidades.filter(unidad__icontains=self.q)
# 			organismos = organismos.filter(organismo__icontains=self.q)
# 			dependencias = dependencias.filter(dependencia__icontains=self.q)
# 			direcciones = direcciones.filter(direccion__icontains=self.q)
# 			departamentos = departamentos.filter(departamento__icontains=self.q)
# 			divisiones = divisiones.filter(division__icontains=self.q)
#
# 		result_list = list(chain(circunscripciones, unidades, organismos, dependencias, direcciones, departamentos, divisiones))
#
# 		return result_list
#
# 	def get_result_value(self, result):
# 		"""Return the value of a result."""
# 		print(type(result))
# 		return str(result.pk)+'-'+str(type(result))

# class FamiliarAutocomplete(autocomplete.Select2QuerySetView):
# 	def get_queryset(self):
# 		# Don't forget to filter out results depending on the visitor !
# 		# if not self.request.user.is_authenticated():
# 		# 	return Familiar.objects.none()

# 		qs = Familiar.objects.all()

# 		if self.q:
# 			qs = qs.filter(nombre__istartswith=self.q)

# 		return qs

# def get_result_label(self, item):
# 	# print('get_result_label: '+item.nombre)
# 	return item.nombre

# def get_selected_result_label(self, item):
# 	# print('Inyectar html en tabla: '+item.nombre)
# 	return ''

# def get_result_value(self, result):
# 	"""Return the value of a result."""
# 	# print('get_result_value:'+result.nombre)
# 	return str(result.pk)

# def post(self, request):
# 	"""Create an object given a text after checking permissions."""
# 	if not self.has_add_permission(request):
# 		return http.HttpResponseForbidden()

# 	if not self.create_field:
# 		raise ImproperlyConfigured('Missing "create_field"')

# 	text = request.POST.get('text', None)

# 	if text is None:
# 		return http.HttpResponseBadRequest()

# 	result = self.create_object(text)
# 	print(result.pk)
# 	return http.JsonResponse({
# 		'id': result.pk,
# 		'text': self.get_result_label(result),
# 	})

# def results(self, results):
# 	"""Return the result dictionary."""
# 	print("results")
# 	return [dict(id=x, text=x) for x in results]