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

