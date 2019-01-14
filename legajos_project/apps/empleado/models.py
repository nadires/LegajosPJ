from django.db import models
from apps.core.models import Signature

from apps.util.models import Seccion

class Empleado(Signature):	
	TIPO_DOC = (
		('DU', 'Documento Único'),
		('LE', 'Libreta de Enrolamiento'),
		('LC', 'Libreta Cívica'),
		('OT', 'Otro'),
	)
	SEXO = (
		('F', 'Femenino'),
		('M', 'Masculino'),
	)

    # DATOS PERSONALES
	apellido = models.CharField(max_length=200)
	nombre = models.CharField(max_length=200)
	tipo_doc = models.CharField(max_length=2, choices=TIPO_DOC, default='DU')
	documento = models.PositiveIntegerField(max_length=10)
	cuil = models.CharField(max_length=15)
	sexo = models.CharField(max_length=1, choices=SEXO)
	

	# DATOS LABORALES
	legajo = models.PositiveIntegerField()

	def __str__(self):
		return '{}, {}'.format(self.apellido, self.nombre)

	class Meta:
		ordering = ('apellido', 'nombre',)

	def images_count(self):
		empleado = Empleado.objects.get(pk=self.pk)
		cantidad = empleado.imagenes_empleado.all().count()
		return cantidad


# Obtiene la sección Otros para asignar por defecto a la imagen al eliminar, si no encuentra la crea 
def  default_seccion ():
    seccion= Seccion.objects.get ( nombre_seccion='Otros')
    if not seccion:
        seccion.nombre_seccion = 'Otros'
        seccion.orden = 5
        seccion.save ()
    return seccion


# Genera una url con el formato /media/empleado/(nro_legajo)/nombre_archivo.jpg
def url_upload_to(instance, filename):
		return '/'.join(['empleado/%s/' %instance.empleado.legajo, filename])
		

class ImagenEmpleado(Signature):
	imagen = models.ImageField(upload_to=url_upload_to)
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='imagenes_empleado')
	seccion = models.ForeignKey(Seccion, on_delete=models.SET(default_seccion), related_name='imagenes_seccion')
	fecha_subida = models.DateTimeField(auto_now_add = True, editable = False)

	class Meta:
		verbose_name = ('Imagen')
		verbose_name_plural = ('Imágenes')

	def __str__(self):
		return '{} - {} {} - {}'.format(self.empleado.legajo, self.empleado.apellido, self.empleado.nombre, self.seccion.nombre_seccion)
