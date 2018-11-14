from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
import json
from django.conf import settings

from .models import Persona, Seccion, Imagen
from .forms import PersonaForm, ImagenForm

from easy_pdf.views import PDFTemplateResponseMixin


def index(request):
	return render(request, 'login.html')


class PersonaList(ListView):
	model = Persona
	template_name = 'legajos/listado_personas.html'
	context_object_name = 'listado_personas'


class PersonaDetail(DetailView):
	model = Persona
	template_name = 'legajos/detalle_persona.html'
	context_object_name = 'persona'

	def get_context_data(self, **kwargs):
		context = super(PersonaDetail, self).get_context_data(**kwargs)
		from apps.persona.models import Seccion
		secciones = Seccion.objects.all() # Busco todas las secciones 
		listado = [] # Listado que contendrá los diccionarios
		for seccion in secciones: # Recorro el listado de secciones
			elemento = {} # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
			elemento['seccion'] = seccion
			id_persona = self.kwargs.get('pk', 0) # Obtengo el id de la persona
			elemento['cantidad_imagenes'] = seccion.cantidad_imagenes_por_seccion(id_persona)
			listado.append(elemento) # Agrego el diccionario a la lista a retornar
	
		context['seccion_list'] = listado
		return context


class PersonaCreate(CreateView):
	model = Persona
	form_class = PersonaForm
	template_name = 'legajos/persona_form.html'

	def get_success_url(self, **kwargs):
		return reverse_lazy('persona_detail', args=[self.object.id])

	def get_context_data(self, **kwargs):
		context = super(PersonaCreate, self).get_context_data(**kwargs)	
		context['titulo'] = "Agregar Empleado"
		return context

	def form_valid(self, form):
		user = self.request.user
		instance = form.save(commit=False)
		if not instance.pk:
			instance.created_by = user
			instance.modified_by = user
		instance.save()
		form.save_m2m()
		return super().form_valid(form)


class PersonaUpdate(UpdateView):
	model = Persona
	form_class = PersonaForm
	template_name = 'legajos/persona_form.html'

	def get_success_url(self, **kwargs):
		return reverse_lazy('persona_detail', args=[self.object.id])

	def get_context_data(self, **kwargs):
		context = super(PersonaUpdate, self).get_context_data(**kwargs)	
		context['titulo'] = "Modificar Empleado"
		return context

	def form_valid(self, form):
		user = self.request.user
		instance = form.save(commit=False)
		instance.modified_by = user
		instance.save()
		form.save_m2m()
		return super().form_valid(form)


class PersonaDelete(DeleteView):
	model = Persona
	template_name = 'legajos/eliminar_persona.html'
	success_url = reverse_lazy('persona_list')
	context_object_name = 'persona'



# class ListadoSeccionesView(View):
# 	def get(self, request, *args, **kwargs):
# 		from apps.persona.models import Seccion
# 		secciones = Seccion.objects.all() # Busco todas las secciones 
# 		listado = [] # Listado que contendrá los diccionarios
# 		for seccion in secciones: # Recorro el listado de secciones
# 			elemento = {} # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
# 			elemento['seccion'] = seccion
# 			id_persona = self.kwargs.get('pk', 0) # Obtengo el id de la persona
# 			elemento['cantidad_imagenes'] = seccion.cantidad_imagenes_por_seccion(id_persona)
# 			listado.append(elemento) # Agrego el diccionario a la lista a retornar
	
# 		# context['seccion_list'] = listado
# 		return JsonResponse(listado)


class ImagenesPersonaView(View):
	def get(self, request, *args, **kwargs):
		id_persona = self.kwargs.get('id_persona', 0)
		id_seccion = self.kwargs.get('id_seccion', 0)
		persona = Persona.objects.get(pk=id_persona)
		seccion = Seccion.objects.get(pk=id_seccion)
		imagenes_list = Imagen.objects.filter(persona=persona, seccion=seccion)
		secciones = Seccion.objects.all()
		listado = [] # Listado que contendrá los diccionarios
		for elem_seccion in secciones: # Recorro el listado de secciones
			elemento = {} # Creo un diccionario por cada seccion guardando el nombre y la cantidad de imagenes que tiene
			elemento['seccion'] = elem_seccion
			elemento['cantidad_imagenes'] = elem_seccion.cantidad_imagenes_por_seccion(id_persona)
			listado.append(elemento) # Agrego el diccionario a la lista a retornar
		context = {
					'imagenes_list': imagenes_list,
					'persona' : persona,
					'seccion' : seccion,
					'seccion_list' : listado,
					}
		return render(self.request, 'legajos/imagenes_persona.html', context)


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


class PersonaPDF(PDFTemplateResponseMixin, DetailView):
	model = Persona
	template_name = 'legajos/pdf.html'
	context_object_name = 'persona'
	base_url = 'file://{}/'.format(settings.STATIC_ROOT)
	download_filename = 'LegajoDigital.pdf'

	def get_context_data(self, **kwargs):
		context = super(PersonaPDF, self).get_context_data(**kwargs)
		id_persona = self.kwargs.get('pk', 0)
		persona = Persona.objects.get(pk=id_persona)
		imagenes_list = Imagen.objects.filter(persona=persona)
		context['imagenes_list'] = imagenes_list
		return context
