from django.db import models


class ActivesManager(models.Manager):
    def get_queryset(self, queryset=None):
        qs = super().get_queryset()
        return qs.filter(is_active=True)