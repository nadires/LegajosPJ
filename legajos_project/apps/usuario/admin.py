from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class UsuarioAdmin(BaseUserAdmin):
    search_fields = ('email',)
    # The forms to add and change user instances
    form = UserAdminChangeForm  # update view
    add_form = UserAdminCreationForm  # create view
    change_password_form = auth_admin.AdminPasswordChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'apellido', 'nombre', 'tipo', 'admin', 'staff', 'active', 'superuser')
    list_filter = ('admin', 'active', 'staff')

    # date_hierarchy = 'fecha_creacion' #Pone el filtro de fechas en el listado de usuarios
    fieldsets = (
        (None, {'fields': ('email', 'password', 'nombre', 'apellido', 'sexo', 'tipo', 'foto',)}),
        ('Permisos', {'fields': ('superuser','admin', 'active', 'staff',)}),
        ('Registros de fechas', {'fields': ('fecha_creacion', 'modified_on')}),
    )
    readonly_fields = ('fecha_creacion', 'modified_on',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'contrasenia1', 'contrasenia2', 'nombre', 'apellido', 'sexo', 'tipo', 'foto')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Usuario, UsuarioAdmin)

# admin.site.unregister(Group)

