from django.contrib import admin

from .models import Empleado, HorarioLaboral

from apps.cargo.models import Cargo, TipoCargo, NivelCargo, AgrupamientoCargo, TipoInstrumentoLegalCargo
from apps.dependencia.models import DependenciaLaboral, Circunscripcion, Unidad, Organismo, Dependencia, Direccion, \
                    Departamento, Division, TipoInstrumentoLegalDependencia

from django.contrib.contenttypes.admin import GenericTabularInline


class CargoInline(GenericTabularInline):
    model = Cargo
    extra = 1


class DependenciaLaboralInline(GenericTabularInline):
    model = DependenciaLaboral
    extra = 1


class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'cuil', 'legajo', 'activo', 'borrado')
    list_filter = ('sexo', 'activo', 'borrado')
    search_fields = ['apellido', 'nombre', 'activo', 'borrado']
    readonly_fields = ('created_on', 'created_by', 'modified_on', 'modified_by', 'activo', 'borrado')

    fieldsets = (
        ('Datos Personales', {'fields': ('apellido', 'nombre', 'tipo_doc', 'documento', 'cuil', 
                                'sexo', 'fecha_nac', 'estado_civil', 'nacionalidad', 'lugar_nac', 
                                'tel_fijo', 'tel_cel', 'email', 'foto_perfil')}),
        ('Domicilio', {'fields': ('domicilio', 'barrio', 'piso', 'dpto', 
                                    'localidad', 'cod_postal', 'departamento', 'provincia')}),
        ('Datos Laborales', {'fields': ('legajo', 'fecha_ingreso', 
                                'estado_laboral', 'fecha_cambio_estado_lab', 'horario')}),
        ('Datos Extras', {'fields': ('fecha_baja', 'motivo_baja', 'created_on', 'created_by', 'modified_on', 'modified_by', 
                            'activo', 'borrado')}),
    )

    inlines = (
        CargoInline,
        DependenciaLaboralInline,
    )

    search_fields = ('apellido', 'nombre', 'activo', 'borrado')

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user        
        instance.modified_by = user	
        instance.save()
        form.save_m2m()
        return instance


# class ImagenesEmpleadosAdmin(admin.ModelAdmin):
#     search_fields = ['imagen']
#     readonly_fields = ('created_on', 'created_by', 'modified_on', 'modified_by', 'fecha_subida',)
#
#     fieldsets = (
#         (None, {'fields': ('imagen', 'persona', 'seccion', 'fecha_subida')}),
#         ('Datos Extras', {'fields': ('created_on', 'created_by', 'modified_on', 'modified_by')}),
#     )
#
#     def save_model(self, request, instance, form, change):
#         user = request.user
#         instance = form.save(commit=False)
#         if not change or not instance.created_by:
#             instance.created_by = user
#             instance.modified_by = user
#             return instance
#         instance.save()
#         form.save_m2m()


admin.site.register(Empleado, EmpleadosAdmin)
# admin.site.register(ImagenEmpleado, ImagenesEmpleadosAdmin)

admin.site.register(HorarioLaboral)
admin.site.register(Cargo)
admin.site.register(TipoCargo)
admin.site.register(NivelCargo)
admin.site.register(AgrupamientoCargo)
admin.site.register(TipoInstrumentoLegalCargo)

admin.site.register(DependenciaLaboral)
admin.site.register(Circunscripcion)
admin.site.register(Unidad)
admin.site.register(Organismo)
admin.site.register(Dependencia)
admin.site.register(Direccion)
admin.site.register(Departamento)
admin.site.register(Division)
admin.site.register(TipoInstrumentoLegalDependencia)
