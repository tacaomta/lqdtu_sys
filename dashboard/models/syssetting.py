from django.db import models


class SystemSetting(models.Model):

    key = models.CharField(
        max_length=100,
        unique=True
    )

    value = models.TextField()

    updated_at = models.DateTimeField(
        auto_now=True
    )

