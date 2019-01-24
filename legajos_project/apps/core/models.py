from django.db import models
from django.conf import settings
from .manager import ActivesManager
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Signature(models.Model):
    class Meta:
        abstract = True

    ''' Defino por defecto que la consulta de empleados es solamente los activos
        Empleado.objects.all() devuelve los empleados con activo=True
        Empleado.todos.all() devuelve todos los empleados
    '''
    objects = models.Manager()
    activos = ActivesManager() 

    activo = models.BooleanField(default=True, editable=False)
    borrado = models.BooleanField(default=False)
    
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
    modified_on = models.DateTimeField(
        auto_now=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created",
        editable=False,
        on_delete=models.CASCADE
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_modified",
        editable=False,
        on_delete=models.CASCADE
    )
