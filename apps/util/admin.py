from django.contrib import admin

from .models import Seccion


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

admin.site.register(Seccion, SeccionesAdmin)
