from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.CharField(
        verbose_name='Адрес', max_length=255, unique=True
    )
    lat = models.FloatField(verbose_name='Широта', null=True, blank=True)
    lon = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    update_at = models.DateTimeField(
        verbose_name='Обновлен', default=timezone.now
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
