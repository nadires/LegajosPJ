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


class AbstractDireccion(models.Model):
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

	DEPARTAMENTOS = (
		('AMB', 'Ambato'),
		('ANC', 'Ancasti'),
		('AND', 'Andalgalá'),
		('ADS', 'Antofagasta de la Sierra'),
		('BEL', 'Belén'),
		('CPY', 'Capayán'),
		('CAP', 'Capital'),
		('EAL', 'El Alto'),
		('FME', 'Fray Mamerto Esquiú'),
		('LPZ', 'La Paz'),
		('PAC', 'Paclín'),
		('PMN', 'Pomán'),
		('SMA', 'Santa María'),
		('SRO', 'Santa Rosa'),
		('TIN', 'Tinogasta'),
		('VVI', 'Valle Viejo'),
		('OTR', 'Otro'),
	)

	class Meta:
		abstract = True

	domicilio = models.TextField()
	barrio = models.TextField(null=True, blank=True)
	piso = models.CharField(max_length=3, null=True, blank=True)
	dpto = models.CharField(max_length=3, null=True, blank=True)
	localidad = models.TextField()
	cod_postal = models.PositiveIntegerField()
	departamento = models.CharField(max_length=3, choices=DEPARTAMENTOS)
	provincia = models.CharField(max_length=2, choices=PROVINCIAS, default='CA')

	def __str__(self):
		return '{}'.format(self.domicilio)
