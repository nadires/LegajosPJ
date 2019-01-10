from django.db import models
from django.conf import settings
from .manager import ActivesManager
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Signature(models.Model):
    class Meta:
        abstract = True

    objects = models.Manager()
    actives = ActivesManager()

    is_active = models.BooleanField(
        default=True,
        editable=False
    )
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