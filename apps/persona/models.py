from django.db import models
from apps.core.models import Signature
import os
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Familiar(models.Model):
	nombre = models.CharField(max_length=200)
	parentesco = models.CharField(max_length=100)

	def __str__(self):
		return '{} - {}'.format(self.nombre, self.parentesco)

class Persona(Signature):	
	apellido = models.CharField(max_length=200)
	nombre = models.CharField(max_length=200)
	cuil = models.CharField(max_length=15)
	dni = models.CharField(max_length=10)
	legajo = models.IntegerField()
	familiares = models.ManyToManyField(Familiar, related_name='personas_familiar')

	def __str__(self):
		return '{}, {}'.format(self.apellido, self.nombre)

	class Meta:
		ordering = ('apellido', 'nombre',)

	def images_count(self):
		persona = Persona.objects.get(pk=self.pk)
		cantidad = persona.imagenes_persona.all().count()
		return cantidad


class Seccion(Signature):
	nombre_seccion = models.CharField(max_length=100)
	orden = models.IntegerField()

	class Meta:
		verbose_name = ('Sección')
		verbose_name_plural = ('Secciones')
		ordering = ('orden',)

	def __str__(self):
		return '{}'.format(self.nombre_seccion)

	# Recibe el id de la persona para filtrar la cantidad de imagenes por seccion por persona
	def cantidad_imagenes_por_seccion(self, persona): 
		seccion = Seccion.objects.get(pk=self.pk)
		cantidad = seccion.imagenes_seccion.filter(persona=persona).count()
		return cantidad


# Obtiene la sección Otros para asignar por defecto a la imagen al eliminar, si no encuentra la crea 
def  default_seccion ():
    seccion= Seccion.objects.get ( nombre_seccion='Otros')
    if not seccion:
        seccion.nombre_seccion = 'Otros'
        seccion.orden = 5
        seccion.save ()
    return seccion


# Genera una url con el formato /media/persona/(nro_legajo)/nombre_archivo.jpg
def url_upload_to(instance, filename):
		return '/'.join(['persona/%s/' %instance.persona.legajo, filename])


class Imagen(Signature):
	imagen = models.ImageField(upload_to=url_upload_to)
	persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='imagenes_persona')
	seccion = models.ForeignKey(Seccion, on_delete=models.SET(default_seccion), related_name='imagenes_seccion')
	fecha_subida = models.DateTimeField(auto_now_add = True, editable = False)

	class Meta:
		verbose_name = ('Imagen')
		verbose_name_plural = ('Imágenes')

	def __str__(self):
		return '{} - {} {} - {}'.format(self.persona.legajo, self.persona.apellido, self.persona.nombre, self.seccion.nombre_seccion)



