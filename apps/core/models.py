from django.db import models
from django.conf import settings
from .manager import ActivesManager
from django.contrib.auth import get_user_model

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
        null=True,
        blank=True
    )
    modified_on = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        get_user_model(),
        related_name="%(class)s_created",
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL
    )
    modified_by = models.ForeignKey(
        get_user_model(),
        related_name="%(class)s_modified",
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL
    )
