from django.db import models
from django.db.models import Manager


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')

    # objects = Manager()

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return self.name
