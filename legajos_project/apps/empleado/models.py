from django.db import models
from apps.core.models import Signature

from apps.util.models import Seccion, AbstractDireccion

class HorarioLaboral(models.Model):
	ingreso = models.TimeField()
	salida = models.TimeField()

	def __str__(self):
		return '{} a {}'.format(
								self.ingreso.isoformat(timespec='minutes'), 
								self.salida.isoformat(timespec='minutes')
								)

	class Meta:
		verbose_name_plural = ('Horarios Laborales')


class Empleado(Signature, AbstractDireccion):	
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
	ESTADO_CIVIL = (
		('CA', 'Casado/a'),
		('CO', 'Comprometido/a'),
		('DI', 'Divorciado/a'),
		('SO', 'Soltero/a'),
		('VI', 'Viudo/a'),
	)
	ESTADO_LABORAL = (
		('AC', 'Activo'),
		('JU', 'Jubilado'),
		('SGH', 'S/G de Haberes'),
		('BA', 'Baja'),
		('SU', 'Suspendido'),
	)

    # DATOS PERSONALES
	apellido = models.CharField(max_length=200)
	nombre = models.CharField(max_length=200)
	tipo_doc = models.CharField(max_length=2, choices=TIPO_DOC, default='DU')
	documento = models.PositiveIntegerField()
	cuil = models.CharField(max_length=15)
	sexo = models.CharField(max_length=1, choices=SEXO, default='M')
	fecha_nac = models.DateField('Fecha de Nacimiento', blank=True, null=True)
	estado_civil = models.CharField(max_length=2, choices=ESTADO_CIVIL, blank=True, null=True)
	nacionalidad = models.TextField(blank=True, null=True)
	lugar_nac = models.TextField('Lugar de Nacimiento', blank=True, null=True)
	tel_fijo = models.CharField('Teléfono Fijo', max_length=17, blank=True, null=True)
	tel_cel = models.CharField('Teléfono Celular', max_length=17, blank=True, null=True)
	email = models.EmailField('E-mail', blank=True, null=True)
	

	# DATOS LABORALES
	legajo = models.PositiveIntegerField()
	fecha_ingreso = models.DateField('Fecha de Ingreso', blank=True, null=True)
	estado_laboral = models.CharField(max_length=3, choices=ESTADO_LABORAL, default='AC', blank=True, null=True)
	fecha_cambio_estado_lab = models.DateField('Fecha de cambio de Estado Laboral', auto_now_add=True, blank=True, null=True)
	horario = models.ForeignKey(HorarioLaboral, on_delete=models.SET_NULL, related_name="empleados_horario", blank=True, null=True)

	def __str__(self):
		return self.get_nombre_completo

	@property
	def get_nombre_completo(self):
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
