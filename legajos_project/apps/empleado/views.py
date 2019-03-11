from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
import json
from django.conf import settings
from datetime import datetime

from .models import Empleado, Cargo, ImagenEmpleado
from apps.util.models import Seccion
from .forms import EmpleadoForm, CargoForm

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
		listado = []  # Listado que contendrá los diccionarios
		for seccion in secciones:  # Recorro el listado de secciones
			elemento = {
				'seccion': seccion}  # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
			id_empleado = self.kwargs.get('pk', 0) # Obtengo el id de la empleado
			elemento['cantidad_imagenes'] = seccion.cantidad_imagenes_por_seccion(id_empleado)
			listado.append(elemento)  # Agrego el diccionario a la lista a retornar
	
		context['seccion_list'] = listado
		contenttype_obj = ContentType.objects.get_for_model(self.object)
		# Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo = None
		try:
			cargo = Cargo.objects.get(object_id=self.object.id, content_type=contenttype_obj, actual=True)
		except Cargo.DoesNotExist:
			cargo = None
		context['cargo'] = cargo
		context['EmpleadoDetail'] = True
		context['titulo'] = "Detalle del Empleado"
		return context


class EmpleadoCreate(SuccessMessageMixin, CreateView):
	model = Empleado
	form_class = EmpleadoForm
	template_name = 'empleado/empleado_form.html'
	success_message = "¡%(calculated_field)s con éxito!"

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
	success_message = "¡%(calculated_field)s con éxito!"

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
			Modifico el método eliminar, haciendo que cambie los estados de borrado y activo
		"""
		self.object = self.get_object()
		self.object.borrado = True
		self.object.activo = False
		self.object.fecha_baja = datetime.strptime(request.POST.get('fecha_baja'), "%d/%m/%Y")
		self.object.motivo_baja = request.POST.get('motivo')
		# print(self.object.fecha_baja)
		# Debería poner fecha de fin al cargo
		self.object.save()
		if self.object.sexo == 'M':
			mensaje = '¡El empleado '+self.object.nombre+' '+self.object.apellido+' fue dado de baja con éxito!'
		else:
			mensaje = '¡La empleada '+self.object.nombre+' '+self.object.apellido+' fue dada de baja con éxito!'
		messages.success(self.request, mensaje)
		return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(EmpleadoDown, self).get_context_data(**kwargs)
		contenttype_obj = ContentType.objects.get_for_model(self.object)
		# Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo = None
		try:
			cargo = Cargo.objects.get(object_id=self.object.id, content_type=contenttype_obj, actual=True)
		except Cargo.DoesNotExist:
			cargo = None
		context['cargo'] = cargo
		context['EmpleadoDown'] = True
		context['titulo'] = "Baja Empleado"
		return context


class EmpleadoRestore(SuccessMessageMixin, UpdateView):
	model = Empleado
	form_class = EmpleadoForm
	template_name = 'empleado/empleado_form.html'
	success_message = "¡%(calculated_field)s con éxito!"

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


# --------------------------------- CARGOS ------------------------------------------------------
class CargoCreate(SuccessMessageMixin, CreateView):
	model = Cargo
	form_class = CargoForm
	template_name = 'empleado/cargo_form.html'
	success_message = "¡El cargo fue agregado con éxito!"

	def get_success_url(self, **kwargs):
		return reverse_lazy('empleado_detail', args=[self.object.object_id])

	def get_context_data(self, **kwargs):
		context = super(CargoCreate, self).get_context_data(**kwargs)	
		id_empleado = self.kwargs.get('pk', 0)
		empleado = Empleado.objects.get(pk=id_empleado)
		context['empleado'] = empleado
		contenttype_obj = ContentType.objects.get_for_model(Empleado)
		# Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo_anterior = None
		try:
			cargo_anterior = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
		except Cargo.DoesNotExist:
			cargo_anterior = None
		context['cargo_anterior'] = cargo_anterior
		context['titulo'] = "Agregar Cargo"
		context['CargoCreate'] = True
		return context

	def form_valid(self, form, **kwargs):
		user = self.request.user
		instance = form.save(commit=False)
		instance.created_by = user
		instance.modified_by = user
		id_empleado = self.kwargs.get('pk', 0)
		empleado = Empleado.objects.get(pk=id_empleado)
		contenttype_obj = ContentType.objects.get_for_model(Empleado)
		try:
			# Busco el cargo anterior para ponerle actual = False, ya que el nuevo cargo será el actual
			cargo_anterior = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
			cargo_anterior.actual = False
			if self.request.POST.get('fecha_fin_cargo_anterior'):
				cargo_anterior.fecha_fin_cargo = datetime.strptime(self.request.POST.get('fecha_fin_cargo_anterior'), "%d/%m/%Y")
			cargo_anterior.save()
		except Cargo.DoesNotExist:
			cargo = None
		instance.object_id = empleado.id
		instance.content_type = contenttype_obj
		instance.save()
		form.save_m2m()
		return super().form_valid(form)


class CargoUpdate(SuccessMessageMixin, UpdateView):
	model = Cargo
	form_class = CargoForm
	template_name = 'empleado/cargo_form.html'
	success_message = "¡El cargo fue modificado con éxito!"

	def get_success_url(self, **kwargs):
		return reverse_lazy('empleado_detail', args=[self.object.object_id])

	def get_context_data(self, **kwargs):
		context = super(CargoUpdate, self).get_context_data(**kwargs)	
		id_empleado = self.kwargs.get('id_empleado', 0)
		empleado = Empleado.objects.get(pk=id_empleado)
		context['empleado'] = empleado
		context['titulo'] = "Modificar Cargo"
		context['CargoUpdate'] = True
		return context

	def form_valid(self, form, **kwargs):
		user = self.request.user
		instance = form.save(commit=False)
		instance.created_by = user
		instance.modified_by = user
		id_empleado = self.kwargs.get('id_empleado', 0)
		empleado = Empleado.objects.get(pk=id_empleado)
		contenttype_obj = ContentType.objects.get_for_model(Empleado)
		try:
			# Busco el cargo anterior para ponerle actual = False, ya que el nuevo cargo será el actual
			cargo_anterior = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
			cargo_anterior.actual = False
			if self.request.POST.get('fecha_fin_cargo_anterior'):
				cargo_anterior.fecha_fin_cargo = datetime.strptime(self.request.POST.get('fecha_fin_cargo_anterior'), "%d/%m/%Y")
			cargo_anterior.save()
		except Cargo.DoesNotExist:
			cargo = None
		instance.object_id = empleado.id
		instance.content_type = contenttype_obj
		instance.save()
		form.save_m2m()
		return super().form_valid(form)


class FojaServicios(DetailView):
	model = Empleado
	template_name = 'empleado/foja_servicios.html'
	context_object_name = 'empleado'

	def get_context_data(self, **kwargs):
		context = super(FojaServicios, self).get_context_data(**kwargs)

		contenttype_obj = ContentType.objects.get_for_model(self.object)
		cargos = Cargo.objects.filter(object_id=self.object.id, content_type=contenttype_obj).order_by('-fecha_ingreso_cargo')
		context['cargos'] = cargos
		context['FojaServicios'] = True
		context['titulo'] = "Foja de Servicios"
		return context

# class ListadoSeccionesView(View):
# 	def get(self, request, *args, **kwargs):
# 		from apps.empleado.models import Seccion
# 		secciones = Seccion.objects.all() # Busco todas las secciones 
# 		listado = [] # Listado que contendrá los diccionarios
# 		for seccion in secciones: # Recorro el listado de secciones
# 			elemento = {} # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
# 			elemento['seccion'] = seccion
# 			id_empleado = self.kwargs.get('pk', 0) # Obtengo el id de la empleado
# 			elemento['cantidad_imagenes'] = seccion.cantidad_imagenes_por_seccion(id_empleado)
# 			listado.append(elemento) # Agrego el diccionario a la lista a retornar
	
# 		# context['seccion_list'] = listado
# 		return JsonResponse(listado)


class ImagenesEmpleadoView(View):
	def get(self, request, *args, **kwargs):
		id_empleado = self.kwargs.get('id_empleado', 0)
		id_seccion = self.kwargs.get('id_seccion', 0)
		empleado = Empleado.objects.get(pk=id_empleado)
		seccion = Seccion.objects.get(pk=id_seccion)
		imagenes_list = ImagenEmpleado.objects.filter(empleado=empleado, seccion=seccion)
		secciones = Seccion.objects.all()
		listado = [] # Listado que contendrá los diccionarios
		for elem_seccion in secciones: # Recorro el listado de secciones
			elemento = {'seccion': elem_seccion, 'cantidad_imagenes': elem_seccion.cantidad_imagenes_por_seccion(
				id_empleado)}  # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
			listado.append(elemento) # Agrego el diccionario a la lista a retornar
		context = {
					'imagenes_list': imagenes_list,
					'empleado' : empleado,
					'seccion' : seccion,
					'seccion_list' : listado,
					}
		return render(self.request, 'empleado/imagenes_empleado.html', context)

	def post(self, request, *args, **kwargs):
		form = ImagenForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			imagen = form.save(commit=False)
			imagen.created_by = request.user
			imagen.modified_by = request.user
			imagen.save()
			form.save_m2m()
			data = {'mensaje':'Success', 'is_valid': True, 'name': imagen.imagen.name, 'url': imagen.imagen.url}
		else:
			data = {'mensaje':'Error', 'is_valid': False}
		return JsonResponse(data)


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
		imagenes_list = ImagenEmpleado.objects.filter(empleado=empleado)
		context['imagenes_list'] = imagenes_list
		return context


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