from django.contrib import admin

from apps.persona.models import Persona, Seccion, Imagen

class PersonasAdmin(admin.ModelAdmin):
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


class SeccionesAdmin(admin.ModelAdmin):
    search_fields = ['nombre_seccion']
    readonly_fields = ('created_on', 'created_by', 'modified_on', 'modified_by',)

    fieldsets = (
        (None, {'fields': ('nombre_seccion', 'orden')}),
        ('Datos Extras', {'fields': ('created_on', 'created_by', 'modified_on', 'modified_by')}),
    )
    

    search_fields = ('nombre_seccion',)

    def save_model(self, request, instance, form, change):
    	user = request.user
    	instance = form.save(commit=False)
    	if not change or not instance.created_by:
    		instance.created_by = user
    		instance.modified_by = user
    		return instance
    	instance.save()
    	form.save_m2m()


class ImagenesAdmin(admin.ModelAdmin):
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


admin.site.register(Persona, PersonasAdmin)
admin.site.register(Seccion, SeccionesAdmin)
admin.site.register(Imagen, ImagenesAdmin)
