import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


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
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    id_dependencia = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    object_id = models.TextField(null=True, blank=True)
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
