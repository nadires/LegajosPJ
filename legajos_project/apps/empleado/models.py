from django.db import models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from apps.core.models import Signature

from apps.util.models import Seccion, AbstractDireccion

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from apps.cargo.models import Cargo


class Circunscripcion(models.Model):
	circunscripcion = models.TextField()

	def __str__(self):
		return self.circunscripcion

	def get_class(self):
		return 'Circunscripción'

	class Meta:
		ordering = ('circunscripcion',)
		verbose_name = 'Circunscripción'
		verbose_name_plural = 'Circunscripciones'


class Unidad(models.Model):
	unidad = models.TextField()
	circunscripcion = models.ForeignKey(Circunscripcion, on_delete=models.SET_NULL, related_name="unidades_circunscripcion", null=True)

	def __str__(self):
		return self.unidad

	def get_class(self):
		return 'Unidad'

	class Meta:
		ordering = ('unidad',)
		verbose_name = 'Unidad'
		verbose_name_plural = 'Unidades'


class Organismo(models.Model):
	organismo = models.TextField()
	unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, related_name="organismos_unidad", null=True)

	def __str__(self):
		return self.organismo

	def get_class(self):
		return 'Organismo'

	class Meta:
		ordering = ('organismo',)


class Dependencia(models.Model):
	dependencia = models.TextField()
	organismo = models.ForeignKey(Organismo, on_delete=models.SET_NULL, related_name="dependencias_organismo", null=True)

	def __str__(self):
		return self.dependencia

	def get_class(self):
		return 'Dependencia'

	class Meta:
		ordering = ('dependencia',)


class Direccion(models.Model):
	direccion = models.TextField()
	dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, related_name="direcciones_dependencia", null=True)

	def __str__(self):
		return self.direccion

	def get_class(self):
		return 'Dirección'

	class Meta:
		ordering = ('direccion',)
		verbose_name = 'Dirección'
		verbose_name_plural = 'Direcciones'


class Departamento(models.Model):
	departamento = models.TextField()
	direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, related_name="ddepartamentos_direccion", null=True)

	def __str__(self):
		return self.departamento

	def get_class(self):
		return 'Departamento'

	class Meta:
		ordering = ('departamento',)


class Division(models.Model):
	division = models.TextField()
	departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, related_name="divisiones_departamento", null=True)

	def __str__(self):
		return self.division

	def get_class(self):
		return 'División'

	class Meta:
		ordering = ('division',)
		verbose_name = 'División'
		verbose_name_plural = 'Divisiones'


class TipoInstrumentoLegalDependencia(models.Model):
	# Resolucion, Pleno, Decreto, Acordada, etc.
	tipo_instrumento = models.TextField()

	def __str__(self):
		return self.tipo_instrumento

	class Meta:
		ordering = ('tipo_instrumento',)
		verbose_name_plural = 'Tipos Instrumentos Legales Dependencias'


class DependenciaLaboral(models.Model):
	circunscripcion = models.ForeignKey(Circunscripcion, on_delete=models.SET_NULL, related_name="dependencias_circunscripcion", null=True, blank=True)
	unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, related_name="dependencias_unidad", null=True, blank=True)
	organismo = models.ForeignKey(Organismo, on_delete=models.SET_NULL, related_name="dependencias_laborales_organismo", null=True, blank=True)
	dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, related_name="dependencias_dependencia", null=True, blank=True)
	direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, related_name="dependencias_direccion", null=True, blank=True)
	departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, related_name="dependencias_departamento", null=True, blank=True)
	division = models.ForeignKey(Division, on_delete=models.SET_NULL, related_name="dependencias_division", null=True, blank=True)
	fecha_ingreso_dependencia = models.DateField('Fecha de ingreso a la Dependencia Laboral', blank=True, null=True)
	instrumento_legal = models.CharField(max_length=20, blank=True)
	tipo_instrumento_legal = models.ForeignKey(TipoInstrumentoLegalDependencia, on_delete=models.SET_NULL, related_name="dependencias_instrumento", null=True)
	fecha_instr_legal = models.DateField('Fecha de instrumento legal', blank=True, null=True)
	actual = models.BooleanField(default=True)

	content_type = models.ForeignKey(
		ContentType,
		limit_choices_to={'model__in': 'empleado'},
		on_delete=models.CASCADE,
		null=True, blank=True
	)
	object_id = models.PositiveIntegerField(null=True, blank=True)
	content_object = GenericForeignKey('content_type', 'object_id')

	def __str__(self):
		if self.division:
			return self.division.division
		if self.departamento:
			return self.departamento.departamento
		if self.direccion:
			return self.direccion.direccion
		if self.dependencia:
			return self.dependencia.dependencia
		if self.organismo:
			return self.organismo.organismo
		if self.unidad:
			return self.unidad.unidad
		return self.circunscripcion.circunscripcion

	class Meta:
		ordering = ('circunscripcion',)
		verbose_name_plural = 'Dependencias Laborales'


# ------------------------------ FIN DEPENDENCIA ----------------------------------------
class HorarioLaboral(models.Model):
	ingreso = models.TimeField()
	salida = models.TimeField()

	def __str__(self):
		return '{} a {}'.format(
			self.ingreso.isoformat(timespec='minutes'),
			self.salida.isoformat(timespec='minutes')
		)

	class Meta:
		verbose_name_plural = 'Horarios Laborales'


# Genera una url con el formato /media/empleado/(nro_legajo)/nombre_archivo.jpg
def url_upload_to(instance, filename):
	return '/'.join(['empleado/%s/' %instance.empleado.legajo, filename])


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
	cuil = models.CharField(max_length=15, unique=True)
	sexo = models.CharField(max_length=1, choices=SEXO, default='M')
	fecha_nac = models.DateField('Fecha de Nacimiento')
	estado_civil = models.CharField(max_length=2, choices=ESTADO_CIVIL)
	nacionalidad = models.TextField()
	lugar_nac = models.TextField('Lugar de Nacimiento')
	tel_fijo = models.CharField('Teléfono Fijo', max_length=17, blank=True, null=True)
	tel_cel = models.CharField('Teléfono Celular', max_length=17, blank=True, null=True)
	email = models.EmailField('E-mail', blank=True, null=True)
	foto_perfil = models.ImageField(upload_to='empleados', blank=True, null=True)

	# DATOS LABORALES
	legajo = models.PositiveIntegerField()
	fecha_ingreso = models.DateField('Fecha de Ingreso')
	estado_laboral = models.CharField(max_length=3, choices=ESTADO_LABORAL, default='AC', blank=True, null=True)
	fecha_cambio_estado_lab = models.DateField('Fecha de cambio de Estado Laboral',  default=date.today, blank=True, null=True)
	horario = models.ForeignKey(HorarioLaboral, on_delete=models.SET_NULL, related_name="empleados_horario", blank=True, null=True)

	# cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, related_name="empleados_cargo", blank=True, null=True)
	cargo = GenericRelation(Cargo, related_query_name='empleados')
	dependencia_laboral = GenericRelation(DependenciaLaboral, related_query_name='empleados')

	fecha_baja = models.DateField('Fecha de baja', blank=True, null=True)
	motivo_baja = models.TextField('Motivo de baja', blank=True)

	def __str__(self):
		return self.get_nombre_completo

	@property
	def get_nombre_completo(self):
		return '{}, {}'.format(self.apellido, self.nombre)

	class Meta:
		ordering = ('apellido', 'nombre',)

	@property
	def edad(self):
		""" retorna la edad si es que tiene cargada una fecha de nacimiento"""
		if self.fecha_nac:
			hoy = datetime.now()
			diff = relativedelta(hoy, self.fecha_nac) 
			return diff.years
		else:
			return ''

	@property
	def antiguedad(self):
		if self.fecha_ingreso:
			hoy = datetime.now()
			diff = relativedelta(hoy, self.fecha_ingreso) 
			antiguedad = '{} años, {} meses, {} días'.format(diff.years, diff.months, diff.days)
			return antiguedad
		else:
			return ''

	def images_count(self):
		empleado = Empleado.objects.get(pk=self.pk)
		cantidad = empleado.imagenes_empleado.all().count()
		return cantidad


# Obtiene la sección Otros para asignar por defecto a la imagen al eliminar, si no encuentra la crea 
def default_seccion():
	seccion = Seccion.objects.get(nombre_seccion='Otros')
	if not seccion:
		seccion.nombre_seccion = 'Otros'
		seccion.orden = 5
		seccion.save()
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
		verbose_name = 'Imagen'
		verbose_name_plural = 'Imágenes'

	def __str__(self):
		return '{} - {} {} - {}'.format(self.empleado.legajo, self.empleado.apellido, self.empleado.nombre, self.seccion.nombre_seccion)
