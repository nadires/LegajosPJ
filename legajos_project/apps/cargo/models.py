from django.db import models

from apps.empleado.models import Empleado


class TipoCargo(models.Model):
    # Es el nombre del cargo en sí, todos los tipos de cargos que existen
    tipo_cargo = models.TextField()

    def __str__(self):
        return self.tipo_cargo

    class Meta:
        ordering = ('tipo_cargo',)
        verbose_name = 'Tipo de Cargo'
        verbose_name_plural = 'Tipos de Cargos'


class NivelCargo(models.Model):
    # Es el nivel para comparar cargos, se utiliza para liquidar sueldos
    nivel = models.TextField()

    def __str__(self):
        return self.nivel

    class Meta:
        ordering = ('nivel',)
        verbose_name_plural = 'Niveles Cargos'


class AgrupamientoCargo(models.Model):
    # Administrativos, Funcionarios, Maestranzas, Magistrados, Pasantes, etc
    agrupamiento = models.TextField()

    def __str__(self):
        return self.agrupamiento

    class Meta:
        ordering = ('agrupamiento',)
        verbose_name_plural = 'Agrupamientos Cargos'


class TipoInstrumentoLegalCargo(models.Model):
    # Resolucion, Pleno, Decreto, Acordada, etc.
    tipo_instrumento = models.TextField()

    def __str__(self):
        return self.tipo_instrumento

    class Meta:
        ordering = ('tipo_instrumento',)
        verbose_name_plural = 'Tipos Instrumentos Legales Cargos'


class Cargo(models.Model):
    SITUACION = (
        ('PP', 'Permanente'),
        ('NP', 'No Permanente'),
        ('CO', 'Contratado'),
        ('PA', 'Pasante'),
        ('OT', 'Otra'),
    )
    JURISDICCION = (
        ('PJ', 'Poder Judicial'),
        ('MP', 'Ministerio Público'),
        ('PO', 'Policia Judicial'),
    )

    empleado = models.ForeignKey(Empleado, related_name="cargos_empleado", on_delete=models.CASCADE)
    cargo = models.ForeignKey(TipoCargo, on_delete=models.SET_NULL, related_name="cargos_tipo", null=True)
    nivel = models.ForeignKey(NivelCargo, on_delete=models.SET_NULL, related_name="cargos_nivel", null=True)
    agrupamiento = models.ForeignKey(AgrupamientoCargo, on_delete=models.SET_NULL, related_name="cargos_agrupamiento", null=True)
    situacion = models.CharField(max_length=2, choices=SITUACION)
    jurisdiccion = models.CharField(max_length=2, choices=JURISDICCION)
    fecha_ingreso_cargo = models.DateField('Fecha de ingreso al cargo', blank=True, null=True)
    fecha_fin_cargo = models.DateField('Fecha de fin del cargo', blank=True, null=True)
    fecha_vencimiento_cargo = models.DateField('Fecha de vencimiento del cargo', blank=True, null=True)
    instrumento_legal = models.CharField(max_length=20, blank=True)
    tipo_instrumento_legal = models.ForeignKey(TipoInstrumentoLegalCargo, on_delete=models.SET_NULL, related_name="cargos_instrumento", null=True)
    fecha_instr_legal = models.DateField('Fecha de instrumento legal', blank=True, null=True)
    actual = models.BooleanField(default=True)

    def __str__(self):
        return self.cargo.tipo_cargo

    class Meta:
        ordering = ('cargo',)
