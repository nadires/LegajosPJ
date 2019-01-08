from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
import json
from django.conf import settings

from .models import Empleado, ImagenEmpleado
from apps.util.models import Seccion
from .forms import EmpleadoForm

from easy_pdf.views import PDFTemplateResponseMixin

from dal import autocomplete
from django.utils.html import format_html


class EmpleadoList(ListView):
	model = Empleado
	template_name = 'empleado/listado_empleados.html'
	context_object_name = 'listado_empleados'


class EmpleadoDetail(DetailView):
	model = Empleado
	template_name = 'empleado/detalle_empleado.html'
	context_object_name = 'empleado'

	def get_context_data(self, **kwargs):
		context = super(EmpleadoDetail, self).get_context_data(**kwargs)
		secciones = Seccion.objects.all() # Busco todas las secciones 
		listado = [] # Listado que contendrá los diccionarios
		for seccion in secciones: # Recorro el listado de secciones
			elemento = {} # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
			elemento['seccion'] = seccion
			id_empleado = self.kwargs.get('pk', 0) # Obtengo el id de la empleado
			elemento['cantidad_imagenes'] = seccion.cantidad_imagenes_por_seccion(id_empleado)
			listado.append(elemento) # Agrego el diccionario a la lista a retornar
	
		context['seccion_list'] = listado
		return context


class EmpleadoCreate(CreateView):
	model = Empleado
	form_class = EmpleadoForm
	template_name = 'empleado/empleado_form.html'

	def get_success_url(self, **kwargs):
		return reverse_lazy('empleado_detail', args=[self.object.id])

	def get_context_data(self, **kwargs):
		context = super(EmpleadoCreate, self).get_context_data(**kwargs)	
		context['titulo'] = "Agregar Empleado"
		return context

	def form_invalid(self, form):
		print(form)
		return self.render_to_response(self.get_context_data(form=form))

	def form_valid(self, form):
		user = self.request.user
		instance = form.save(commit=False)
		if not instance.pk:
			instance.created_by = user
			instance.modified_by = user
		instance.save()
		form.save_m2m()
		return super().form_valid(form)


class EmpleadoUpdate(UpdateView):
	model = Empleado
	form_class = EmpleadoForm
	template_name = 'empleado/empleado_form.html'

	def get_success_url(self, **kwargs):
		return reverse_lazy('empleado_detail', args=[self.object.id])

	def get_context_data(self, **kwargs):
		context = super(EmpleadoUpdate, self).get_context_data(**kwargs)	
		context['titulo'] = "Modificar Empleado"
		return context

	def form_valid(self, form):
		user = self.request.user
		instance = form.save(commit=False)
		instance.modified_by = user
		instance.save()
		form.save_m2m()
		return super().form_valid(form)


class EmpleadoDelete(DeleteView):
	model = Empleado
	template_name = 'empleado/eliminar_empleado.html'
	success_url = reverse_lazy('empleado_list')
	context_object_name = 'empleado'



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
		imagenes_list = Imagen.objects.filter(empleado=empleado, seccion=seccion)
		secciones = Seccion.objects.all()
		listado = [] # Listado que contendrá los diccionarios
		for elem_seccion in secciones: # Recorro el listado de secciones
			elemento = {} # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
			elemento['seccion'] = elem_seccion
			elemento['cantidad_imagenes'] = elem_seccion.cantidad_imagenes_por_seccion(id_empleado)
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
		imagenes_list = Imagen.objects.filter(empleado=empleado)
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