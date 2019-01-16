from django.db import models
from apps.core.models import Signature


class Seccion(Signature):
	nombre_seccion = models.CharField(max_length=100)
	orden = models.IntegerField()

	class Meta:
		verbose_name = ('Sección')
		verbose_name_plural = ('Secciones')
		ordering = ('orden',)

	def __str__(self):
		return '{}'.format(self.nombre_seccion)

	# Recibe el id de la empleado para filtrar la cantidad de imagenes por seccion por empleado
	def cantidad_imagenes_por_seccion(self, empleado): 
		seccion = Seccion.objects.get(pk=self.pk)
		cantidad = seccion.imagenes_seccion.filter(empleado=empleado).count()
		return cantidad


class Provincia(models.Model):
	PROVINCIAS = (
		('BA', 'Buenos Aires'),
		('CA', 'Catamarca'),
		('CH', 'Chaco'),
		('CT', 'Chubut'),
		('CB', 'Cordoba'),
		('CR', 'Corrientes'),
		('ER', 'Entre Rios'),
		('FO', 'Formosa'),
		('JY', 'Jujuy'),
		('LP', 'La Pampa'),
		('LR', 'La Rioja'),
		('MZ', 'Mendoza'),
		('MI', 'Misiones'),
		('NQ', 'Neuquen'),
		('RN', 'Rio Negro'),
		('SA', 'Salta'),
		('SJ', 'San Juan'),
		('SL', 'San Luis'),
		('SC', 'Santa Cruz'),
		('SF', 'Santa Fe'),
		('SE', 'Santiago del Estero'),
		('TF', 'Tierra del Fuego'),
		('TU', 'Tucuman'),
	)

	class Meta:
		ordering = ('nombre',)

	nombre = models.CharField(max_length=2, choices=PROVINCIAS)

	def __str__(self):
		return self.nombre


class Localidad(models.Model):

	class Meta:
		ordering = ('nombre',)
		verbose_name_plural = 'Localidades'

	nombre = models.TextField()
	cod_postal = models.PositiveIntegerField(null=True, blank=True)

	def __str__(self):
		return self.nombre


class AbstractDireccion(models.Model):

	class Meta:
		abstract = True

	domicilio = models.TextField(null=True, blank=True)
	barrio = models.TextField(null=True, blank=True)
	piso = models.CharField(max_length=3, null=True, blank=True)
	dpto = models.CharField(max_length=3, null=True, blank=True)
	localidad = models.ForeignKey(Localidad,null=True, blank=True,on_delete=models.CASCADE)
	provincia = models.ForeignKey(Provincia, null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.domicilio)
