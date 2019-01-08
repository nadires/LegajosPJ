from django.contrib import admin

from .models import Empleado, ImagenEmpleado

class EmpleadosAdmin(admin.ModelAdmin):
    search_fields = ['apellido', 'nombre']
    readonly_fields = ('created_on', 'created_by', 'modified_on', 'modified_by',)

    fieldsets = (
        (None,
         {'fields': ('apellido', 'nombre', 'cuil', 'dni', 'legajo')}),
        ('Datos Extras', {'fields': ('created_on', 'created_by', 'modified_on', 'modified_by')}),
    )

    search_fields = ('apellido', 'nombre',)

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user        
        instance.modified_by = user	
        instance.save()
        form.save_m2m()
        return instance


class ImagenesEmpleadosAdmin(admin.ModelAdmin):
    search_fields = ['imagen']
    readonly_fields = ('created_on', 'created_by', 'modified_on', 'modified_by', 'fecha_subida',)

    fieldsets = (
        (None, {'fields': ('imagen', 'persona', 'seccion', 'fecha_subida')}),
        ('Datos Extras', {'fields': ('created_on', 'created_by', 'modified_on', 'modified_by')}),
    )
    

    def save_model(self, request, instance, form, change):
    	user = request.user
    	instance = form.save(commit=False)
    	if not change or not instance.created_by:
    		instance.created_by = user
    		instance.modified_by = user
    		return instance
    	instance.save()
    	form.save_m2m()


admin.site.register(Empleado, EmpleadosAdmin)
admin.site.register(ImagenEmpleado, ImagenesEmpleadosAdmin)